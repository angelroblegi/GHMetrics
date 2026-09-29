#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT - CARGA DE CONSULTORES DESDE EXCEL

Lee un Excel de consultores, deduplica, traduce el nombre de cada
célula a su Id y los carga al CommanCenter API.

Requisitos:
    pip install pandas openpyxl requests

Uso (en este orden):
    python cargue_excel.py consultores.xlsx --dry-run
        Solo valida y deduplica, NO envía nada. Genera reporte_carga.csv.

    python cargue_excel.py consultores.xlsx --limite 3
        Envía únicamente las 3 primeras filas válidas (prueba con datos reales).

    python cargue_excel.py consultores.xlsx
        Carga completa.

Credenciales:
    Variables de entorno API_USER y API_PASSWORD,
    o el script las solicita por consola.
"""

import argparse
import csv
import getpass
import os
import re
import sys
import time
import unicodedata

import pandas as pd
import requests
import urllib3


# ============================================================
# CONFIGURACIÓN
# ============================================================

# URL de tu API (local por ahora)
API_URL = os.getenv("API_URL", "https://localhost:65002")

# Endpoint de autenticación
LOGIN_PATH = "/api/auth/login"

# Campos definidos en LoginDto
LOGIN_USER_FIELD = "usuario"
LOGIN_PASS_FIELD = "password"

# Endpoints
CONSULTORES_PATH = "/api/consultores"
CELULAS_PATH = "/api/celulas"

# Pausa entre envíos (el API limita solicitudes por minuto)
PAUSA_SEGUNDOS = 1.1

# Si el GET de células falla, o algún nombre del Excel no coincide,
# complétalo aquí manualmente: {"nombre exacto o parecido": id}
CELULAS_MANUAL = {
    # "DataTeam": 1,
}

# Estado con el que se crean todos los registros de esta carga
ESTADO_FIJO = "Activo"

# Certificado SSL autofirmado de localhost: deshabilita la advertencia
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ============================================================
# MAPEO DE COLUMNAS DEL EXCEL
# ============================================================
# Campo del API -> encabezado tal cual aparece en tu Excel.
# La comparación ignora tildes, mayúsculas y espacios, así que
# no hace falta que coincida carácter por carácter.

MAPA_COLUMNAS = {
    "Cedula": "Cedula",
    "Nombre": "Nombre",
    "Apellido": "Apellido",
    "Email": "Email",
    "Celular": "Celular",
    "Cargo": "Cargo",
    "Rol": "Rol",
    "Empresa": "Empresa",
    "Ciudad": "Ciudad",
    "FechaIngreso": "Fecha Ingreso",
    "FechaNacimiento": "Fecha Nacimiento",
    "Direccion": "Direccion",
    "Barrio": "Barrio",
    "ContactoEmergenciaNombre": "ContactoEmergenciaNombre",
    "ContactoEmergenciaTelefono": "ContactoEmergenciaTelefono",
    "Celula": "Celula",
    "PorcentajeParticipacion": "PorcentajeParticipacion",
}

CAMPOS_TEXTO = [
    "Cedula", "Nombre", "Apellido", "Email", "Celular", "Cargo", "Rol",
    "Empresa", "Ciudad", "Direccion", "Barrio",
    "ContactoEmergenciaNombre", "ContactoEmergenciaTelefono",
]
CAMPOS_FECHA = ["FechaIngreso", "FechaNacimiento"]

OBLIGATORIOS = [
    "Cedula", "Nombre", "Apellido", "Email",    
]

MAX_LEN = {
    "Cedula": 30, "Nombre": 100, "Apellido": 100, "Email": 200, "Celular": 20,
    "Cargo": 150, "Rol": 100, "Empresa": 150, "Ciudad": 100, "Direccion": 250,
    "Barrio": 100, "ContactoEmergenciaNombre": 150, "ContactoEmergenciaTelefono": 20,
}


# ============================================================
# UTILIDADES
# ============================================================

def clave(s):
    """Normaliza texto para comparar: sin tildes, minúsculas, sin espacios/símbolos."""
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def vacio(v):
    return (
        v is None
        or (not isinstance(v, str) and pd.isna(v))
        or str(v).strip().lower() in ("", "nan", "none", "nat")
    )


def txt(v):
    return "" if vacio(v) else str(v).strip()


def fecha_iso(v):
    """
    Convierte el valor de la celda a texto ISO (YYYY-MM-DDT00:00:00).

    Colombia escribe las fechas como DD/MM/AAAA, así que SIEMPRE se
    interpreta primero como día/mes/año (dayfirst=True). Por eso
    '5/10/2026' se lee como 5 de octubre de 2026, no como 10 de mayo.

    Si la celda ya viene como fecha real de Excel (pandas la entrega
    como Timestamp en vez de texto), se usa directamente sin volver a
    interpretar el orden día/mes, porque Excel ya la guardó sin
    ambigüedad.

    Devuelve None si la celda está vacía o si el texto no se puede
    interpretar como fecha en absoluto (para eso está el chequeo de
    'no es una fecha válida' en construir_filas).
    """
    if vacio(v):
        return None
    if isinstance(v, pd.Timestamp):
        return v.strftime("%Y-%m-%dT00:00:00")
    d = pd.to_datetime(str(v).strip(), dayfirst=True, errors="coerce")
    return None if pd.isna(d) else d.strftime("%Y-%m-%dT00:00:00")


def fecha_fuera_de_rango(campo, iso):
    """
    Chequeo de cordura, NO de formato. Si la fecha ya se interpretó
    pero cae en un rango imposible para ese campo (ej. alguien nacido
    en 1890, o un ingreso en el año 2090), probablemente el día/mes
    quedaron invertidos en el Excel original. Se reporta para que la
    revises a mano en vez de cargarla en silencio.
    """
    if iso is None:
        return None
    anio = int(iso[:4])
    hoy = pd.Timestamp.today()
    if campo == "FechaIngreso" and not (2000 <= anio <= hoy.year):
        return f"FechaIngreso con año sospechoso ({anio}); revisa si el día/mes están invertidos"
    return None


def porcentaje(v):
    """Devuelve un decimal 0-100 o None si viene vacío o inválido."""
    if vacio(v):
        return None
    s = str(v).strip().replace("%", "").replace(",", ".")
    try:
        num = float(s)
    except ValueError:
        return None
    return num if 0 <= num <= 100 else None


def buscar_token(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key.lower() in ("token", "accesstoken", "access_token", "jwt") and isinstance(value, str):
                return value
        for value in obj.values():
            t = buscar_token(value)
            if t:
                return t
    return None


# ============================================================
# API
# ============================================================

def login():
    user = os.getenv("API_USER") or input("Usuario del API: ").strip()
    pwd = os.getenv("API_PASSWORD") or getpass.getpass("Contraseña del API: ")

    print("\nConectando al API...")
    print(f"URL: {API_URL + LOGIN_PATH}")

    try:
        response = requests.post(
            API_URL + LOGIN_PATH,
            json={LOGIN_USER_FIELD: user, LOGIN_PASS_FIELD: pwd},
            timeout=60,
            verify=False,
        )
    except requests.exceptions.RequestException as e:
        sys.exit(f"\nError conectando con el API durante el login:\n{e}")

    if response.status_code >= 300:
        sys.exit(f"\nLogin falló (HTTP {response.status_code}):\n{response.text[:500]}")

    try:
        data = response.json()
    except ValueError:
        sys.exit(f"\nEl login respondió, pero no es JSON:\n{response.text[:500]}")

    token = buscar_token(data)
    if not token:
        sys.exit(f"\nNo encontré el token en la respuesta del login:\n{response.text[:500]}")

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json"})
    session.verify = False
    print("Login correcto.")
    return session


def cargar_celulas(session):
    """Devuelve {nombre_normalizado: id}, combinando el API con CELULAS_MANUAL."""
    mapa = {}
    try:
        r = session.get(API_URL + CELULAS_PATH, timeout=60)
        data = r.json() if r.status_code < 300 else []
        if isinstance(data, dict):
            data = next((v for v in data.values() if isinstance(v, list)), [])
        for item in data:
            low = {str(k).lower(): v for k, v in item.items()}
            if "id" in low and "nombre" in low:
                mapa[clave(low["nombre"])] = low["id"]
    except Exception as e:  # noqa: BLE001
        print(f"Aviso: no pude leer las células del API ({e}). Uso solo CELULAS_MANUAL.")

    for nombre, cid in CELULAS_MANUAL.items():
        mapa[clave(nombre)] = cid

    print(f"Células conocidas: {len(mapa)}")
    return mapa


def enviar(session, payload):
    for _ in range(4):
        try:
            r = session.post(API_URL + CONSULTORES_PATH, json=payload, timeout=60)
        except requests.exceptions.RequestException as e:
            return False, 0, str(e)
        if r.status_code == 429:
            ra = r.headers.get("Retry-After", "")
            espera = int(ra) if ra.isdigit() else 30
            print(f"  429 (límite de solicitudes). Espero {espera}s y reintento...")
            time.sleep(espera)
            continue
        return r.status_code < 300, r.status_code, r.text[:500]
    return False, 429, "Límite de solicitudes excedido tras reintentos"


# ============================================================
# PROCESO DEL EXCEL
# ============================================================

def construir_filas(df, columnas, celulas_ids):
    filas = []
    for idx, row in df.iterrows():
        p, problemas = {}, []

        for campo in CAMPOS_TEXTO:
            p[campo] = txt(row[columnas[campo]]) if campo in columnas else ""

        for campo in CAMPOS_FECHA:
            crudo = row[columnas[campo]] if campo in columnas else None
            p[campo] = fecha_iso(crudo)
            if not vacio(crudo) and p[campo] is None:
                problemas.append(f"{campo} no es una fecha válida: '{crudo}'")
            else:
                aviso = fecha_fuera_de_rango(campo, p[campo])
                if aviso:
                    problemas.append(aviso)

        p["Email"] = p["Email"].lower()
        p["Estado"] = ESTADO_FIJO

        # Célula por nombre -> id (soporta varias separadas por ; , /)
        col_celula = columnas.get("Celula")
        nombres = [x.strip() for x in re.split(r"[;,/|]", txt(row[col_celula])) if x.strip()] if col_celula else []

        col_pct = columnas.get("PorcentajeParticipacion")
        pct = porcentaje(row[col_pct]) if col_pct else None

        celulas = []
        for nom in nombres:
            cid = celulas_ids.get(clave(nom))
            if cid is None:
                problemas.append(f"Célula no encontrada: '{nom}'")
            else:
                celulas.append({"CelulaId": cid, "PorcentajeParticipacion": pct})
        if not nombres:
            problemas.append("Falta la célula")
        p["Celulas"] = celulas

        for campo in OBLIGATORIOS:
            if not p.get(campo):
                problemas.append(f"Falta {campo}")
        if p["Email"] and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", p["Email"]):
            problemas.append(f"Email con formato inválido: '{p['Email']}'")
        for campo, mx in MAX_LEN.items():
            if len(p.get(campo) or "") > mx:
                problemas.append(f"{campo} supera {mx} caracteres")

        for campo in CAMPOS_TEXTO:  # opcionales vacíos -> null
            if p[campo] == "" and campo not in OBLIGATORIOS:
                p[campo] = None

        filas.append({"fila": idx + 2, "payload": p, "problemas": problemas})
    return filas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("excel", help="ruta del Excel a cargar")
    ap.add_argument("--hoja", default=0, help="hoja (nombre o índice; por defecto la primera)")
    ap.add_argument("--dry-run", action="store_true", help="valida y deduplica sin enviar nada")
    ap.add_argument("--limite", type=int, help="envía solo las primeras N filas válidas")
    args = ap.parse_args()

    df = pd.read_excel(args.excel, sheet_name=args.hoja, dtype=str)
    print(f"Excel leído: {len(df)} filas.")

    por_clave = {clave(c): c for c in df.columns}
    columnas, faltan = {}, []
    for campo, encabezado in MAPA_COLUMNAS.items():
        col = por_clave.get(clave(encabezado))
        if col is None:
            faltan.append(encabezado)
        else:
            columnas[campo] = col
    if faltan:
        sys.exit(f"No encontré estas columnas en el Excel: {faltan}\nColumnas del archivo: {list(df.columns)}")

    session = login()
    celulas_ids = cargar_celulas(session)
    if celulas_ids:
        print("Células reconocidas:", {k: v for k, v in celulas_ids.items()})

    filas = construir_filas(df, columnas, celulas_ids)

    reporte, pendientes = [], []
    vistos_ced, vistos_mail = {}, {}
    for f in filas:
        p = f["payload"]
        base = {
            "fila": f["fila"], "cedula": p["Cedula"], "email": p["Email"],
            "nombre": f"{p['Nombre']} {p['Apellido']}".strip(),
        }
        if f["problemas"]:
            reporte.append({**base, "estado": "INVALIDO", "detalle": "; ".join(f["problemas"])})
            continue

        kc, km = clave(p["Cedula"]), p["Email"]
        #if kc in vistos_ced or km in vistos_mail:
        #    igual = vistos_ced.get(kc) or vistos_mail.get(km)
        #    reporte.append({**base, "estado": "DUPLICADO", "detalle": f"Repite cédula o email de la fila {igual}"})
        #    continue

        vistos_ced[kc] = vistos_mail[km] = f["fila"]
        pendientes.append((f, base))

    n_dup = sum(r["estado"] == "DUPLICADO" for r in reporte)
    n_inv = sum(r["estado"] == "INVALIDO" for r in reporte)
    print(f"Válidas y únicas: {len(pendientes)} | duplicadas: {n_dup} | inválidas: {n_inv}")

    if args.limite:
        pendientes = pendientes[:args.limite]

    if args.dry_run:
        for f, base in pendientes:
            reporte.append({**base, "estado": "LISTO (dry-run)", "detalle": ""})
        print("Dry-run: no se envió nada.")
    else:
        for i, (f, base) in enumerate(pendientes, 1):
            ok, status, detalle = enviar(session, f["payload"])
            reporte.append({**base, "estado": "OK" if ok else "ERROR_API", "detalle": "" if ok else f"HTTP {status}: {detalle}"})
            print(f"[{i}/{len(pendientes)}] fila {f['fila']}: {'OK' if ok else 'ERROR ' + str(status)}")
            time.sleep(PAUSA_SEGUNDOS)

    reporte.sort(key=lambda r: r["fila"])
    with open("reporte_carga.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["fila", "estado", "cedula", "email", "nombre", "detalle"])
        w.writeheader()
        w.writerows(reporte)
    print("Reporte guardado en reporte_carga.csv")


if __name__ == "__main__":
    main()
