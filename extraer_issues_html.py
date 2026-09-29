```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT - CARGA DE CONSULTORES DESDE EXCEL

Lee un Excel de consultores, traduce el nombre de cada
célula a su Id y los carga al CommanCenter API.

IMPORTANTE:
    - Se permiten cédulas duplicadas.
    - Se permiten emails duplicados.
    - Se permiten personas duplicadas.
    - Se permite repetir una célula.
    - No se valida el año de las fechas.
    - Sí se valida que una fecha pueda interpretarse correctamente.

Requisitos:
    pip install pandas openpyxl requests

Uso:

    python cargue_excel.py consultores.xlsx --dry-run
        Solo valida, NO envía nada.
        Genera reporte_carga.csv.

    python cargue_excel.py consultores.xlsx --limite 3
        Envía únicamente las 3 primeras filas válidas.

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

# URL de tu API
API_URL = os.getenv(
    "API_URL",
    "https://localhost:65002"
)

# Endpoint de autenticación
LOGIN_PATH = "/api/auth/login"

# Campos definidos en LoginDto
LOGIN_USER_FIELD = "usuario"
LOGIN_PASS_FIELD = "password"

# Endpoints
CONSULTORES_PATH = "/api/consultores"
CELULAS_PATH = "/api/celulas"

# Pausa entre envíos
PAUSA_SEGUNDOS = 1.1

# Si alguna célula no coincide con las obtenidas del API,
# puedes agregarla manualmente:
#
# CELULAS_MANUAL = {
#     "DataTeam": 1,
# }
CELULAS_MANUAL = {
    # "DataTeam": 1,
}

# Estado con el que se crean todos los registros
ESTADO_FIJO = "Activo"

# Certificado SSL autofirmado de localhost
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# ============================================================
# MAPEO DE COLUMNAS DEL EXCEL
# ============================================================

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
    "Cedula",
    "Nombre",
    "Apellido",
    "Email",
    "Celular",
    "Cargo",
    "Rol",
    "Empresa",
    "Ciudad",
    "Direccion",
    "Barrio",
    "ContactoEmergenciaNombre",
    "ContactoEmergenciaTelefono",
]

CAMPOS_FECHA = [
    "FechaIngreso",
    "FechaNacimiento",
]


# SOLO estos campos son obligatorios.
#
# Celula se valida aparte porque se obtiene
# mediante el nombre de la célula.
OBLIGATORIOS = [
    "Cedula",
    "Nombre",
    "Apellido",
    "Email",
]


MAX_LEN = {
    "Cedula": 30,
    "Nombre": 100,
    "Apellido": 100,
    "Email": 200,
    "Celular": 20,
    "Cargo": 150,
    "Rol": 100,
    "Empresa": 150,
    "Ciudad": 100,
    "Direccion": 250,
    "Barrio": 100,
    "ContactoEmergenciaNombre": 150,
    "ContactoEmergenciaTelefono": 20,
}


# ============================================================
# UTILIDADES
# ============================================================

def clave(s):
    """
    Normaliza texto para comparar:

    - elimina tildes
    - pasa a minúsculas
    - elimina espacios
    - elimina símbolos
    """

    s = (
        unicodedata
        .normalize("NFKD", str(s))
        .encode("ascii", "ignore")
        .decode()
    )

    return re.sub(
        r"[^a-z0-9]",
        "",
        s.lower()
    )


def vacio(v):
    return (
        v is None
        or (
            not isinstance(v, str)
            and pd.isna(v)
        )
        or str(v).strip().lower()
        in ("", "nan", "none", "nat")
    )


def txt(v):
    return "" if vacio(v) else str(v).strip()


# ============================================================
# FECHAS
# ============================================================

def fecha_iso(v):
    """
    Convierte el valor de la celda a:

        YYYY-MM-DDT00:00:00

    Las fechas del Excel se interpretan como:

        DD/MM/AAAA

    Ejemplo:

        5/10/2026
        -> 2026-10-05T00:00:00

    También acepta fechas que pandas/Excel entregue
    directamente como Timestamp.

    Devuelve None si:
        - la celda está vacía
        - el valor no puede interpretarse como fecha
    """

    if vacio(v):
        return None

    # Si Excel ya entregó una fecha real
    if isinstance(v, pd.Timestamp):
        return v.strftime(
            "%Y-%m-%dT00:00:00"
        )

    texto_fecha = str(v).strip()

    if not texto_fecha:
        return None

    try:

        # Si viene en formato ISO:
        #
        # 2026-09-29
        # 2026-09-29 00:00:00
        #
        # no usamos dayfirst=True.
        if re.match(
            r"^\d{4}-\d{1,2}-\d{1,2}",
            texto_fecha
        ):

            d = pd.to_datetime(
                texto_fecha,
                errors="coerce"
            )

        else:

            # Formato colombiano:
            #
            # DD/MM/YYYY
            #
            d = pd.to_datetime(
                texto_fecha,
                dayfirst=True,
                errors="coerce"
            )

        if pd.isna(d):
            return None

        return d.strftime(
            "%Y-%m-%dT00:00:00"
        )

    except Exception:
        return None


def fecha_fuera_de_rango(campo, iso):
    """
    No se realiza ninguna validación del año.

    Por ejemplo, todas estas fechas pueden pasar:

        FechaNacimiento = 2023
        FechaNacimiento = 2025
        FechaNacimiento = 1999

    Mientras el valor pueda interpretarse como una fecha válida.

    También se permite cualquier año para FechaIngreso.

    """

    return None


# ============================================================
# PORCENTAJE
# ============================================================

def porcentaje(v):
    """
    Devuelve un decimal entre 0 y 100.

    Soporta:

        50
        50.5
        50%
        50,5
        50,5%
    """

    if vacio(v):
        return None

    s = (
        str(v)
        .strip()
        .replace("%", "")
        .replace(",", ".")
    )

    try:
        num = float(s)

    except ValueError:
        return None

    return (
        num
        if 0 <= num <= 100
        else None
    )


# ============================================================
# TOKEN
# ============================================================

def buscar_token(obj):

    if isinstance(obj, dict):

        for key, value in obj.items():

            if (
                key.lower()
                in (
                    "token",
                    "accesstoken",
                    "access_token",
                    "jwt",
                )
                and isinstance(value, str)
            ):
                return value

        for value in obj.values():

            t = buscar_token(value)

            if t:
                return t

    return None


# ============================================================
# API - LOGIN
# ============================================================

def login():

    user = (
        os.getenv("API_USER")
        or input("Usuario del API: ").strip()
    )

    pwd = (
        os.getenv("API_PASSWORD")
        or getpass.getpass(
            "Contraseña del API: "
        )
    )

    print("\nConectando al API...")
    print(
        f"URL: {API_URL + LOGIN_PATH}"
    )

    try:

        response = requests.post(
            API_URL + LOGIN_PATH,
            json={
                LOGIN_USER_FIELD: user,
                LOGIN_PASS_FIELD: pwd,
            },
            timeout=60,
            verify=False,
        )

    except requests.exceptions.RequestException as e:

        sys.exit(
            "\nError conectando con el API durante el login:\n"
            f"{e}"
        )

    if response.status_code >= 300:

        sys.exit(
            f"\nLogin falló "
            f"(HTTP {response.status_code}):\n"
            f"{response.text[:500]}"
        )

    try:

        data = response.json()

    except ValueError:

        sys.exit(
            "\nEl login respondió, pero no es JSON:\n"
            f"{response.text[:500]}"
        )

    token = buscar_token(data)

    if not token:

        sys.exit(
            "\nNo encontré el token en la respuesta del login:\n"
            f"{response.text[:500]}"
        )

    session = requests.Session()

    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })

    session.verify = False

    print("Login correcto.")

    return session


# ============================================================
# API - CÉLULAS
# ============================================================

def cargar_celulas(session):
    """
    Devuelve:

        {
            nombre_normalizado: id
        }

    Ejemplo:

        {
            "datateam": 3
        }
    """

    mapa = {}

    try:

        r = session.get(
            API_URL + CELULAS_PATH,
            timeout=60
        )

        data = (
            r.json()
            if r.status_code < 300
            else []
        )

        if isinstance(data, dict):

            data = next(
                (
                    v
                    for v in data.values()
                    if isinstance(v, list)
                ),
                []
            )

        for item in data:

            low = {
                str(k).lower(): v
                for k, v in item.items()
            }

            if (
                "id" in low
                and "nombre" in low
            ):

                mapa[
                    clave(low["nombre"])
                ] = low["id"]

    except Exception as e:

        print(
            "Aviso: no pude leer las células "
            f"del API ({e}). "
            "Uso solo CELULAS_MANUAL."
        )

    # Células manuales
    for nombre, cid in CELULAS_MANUAL.items():

        mapa[
            clave(nombre)
        ] = cid

    print(
        f"Células conocidas: {len(mapa)}"
    )

    return mapa


# ============================================================
# API - ENVIAR
# ============================================================

def enviar(session, payload):

    for _ in range(4):

        try:

            r = session.post(
                API_URL + CONSULTORES_PATH,
                json=payload,
                timeout=60
            )

        except requests.exceptions.RequestException as e:

            return False, 0, str(e)

        if r.status_code == 429:

            ra = r.headers.get(
                "Retry-After",
                ""
            )

            espera = (
                int(ra)
                if ra.isdigit()
                else 30
            )

            print(
                "  429 "
                "(límite de solicitudes). "
                f"Espero {espera}s y reintento..."
            )

            time.sleep(espera)

            continue

        return (
            r.status_code < 300,
            r.status_code,
            r.text[:500],
        )

    return (
        False,
        429,
        "Límite de solicitudes excedido "
        "tras reintentos",
    )


# ============================================================
# PROCESAR EXCEL
# ============================================================

def construir_filas(
    df,
    columnas,
    celulas_ids
):

    filas = []

    for idx, row in df.iterrows():

        p = {}
        problemas = []

        # ----------------------------------------------------
        # CAMPOS DE TEXTO
        # ----------------------------------------------------

        for campo in CAMPOS_TEXTO:

            p[campo] = (
                txt(row[columnas[campo]])
                if campo in columnas
                else ""
            )

        # ----------------------------------------------------
        # FECHAS
        # ----------------------------------------------------

        for campo in CAMPOS_FECHA:

            crudo = (
                row[columnas[campo]]
                if campo in columnas
                else None
            )

            p[campo] = fecha_iso(
                crudo
            )

            # Solo se rechaza si realmente
            # no pudo convertirse en fecha.
            if (
                not vacio(crudo)
                and p[campo] is None
            ):

                problemas.append(
                    f"{campo} no es una fecha válida: "
                    f"'{crudo}'"
                )

            else:

                aviso = fecha_fuera_de_rango(
                    campo,
                    p[campo]
                )

                if aviso:
                    problemas.append(aviso)

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        p["Email"] = p["Email"].lower()

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        p["Estado"] = ESTADO_FIJO

        # ----------------------------------------------------
        # CÉLULAS
        # ----------------------------------------------------

        col_celula = columnas.get(
            "Celula"
        )

        if col_celula:

            nombres = [
                x.strip()
                for x in re.split(
                    r"[;,/|]",
                    txt(row[col_celula])
                )
                if x.strip()
            ]

        else:

            nombres = []

        # ----------------------------------------------------
        # PORCENTAJE
        # ----------------------------------------------------

        col_pct = columnas.get(
            "PorcentajeParticipacion"
        )

        pct = (
            porcentaje(row[col_pct])
            if col_pct
            else None
        )

        # ----------------------------------------------------
        # MAPEAR CÉLULAS
        # ----------------------------------------------------

        celulas = []

        for nom in nombres:

            cid = celulas_ids.get(
                clave(nom)
            )

            if cid is None:

                problemas.append(
                    f"Célula no encontrada: '{nom}'"
                )

            else:

                celulas.append({
                    "CelulaId": cid,
                    "PorcentajeParticipacion": pct,
                })

        if not nombres:

            problemas.append(
                "Falta la célula"
            )

        p["Celulas"] = celulas

        # ----------------------------------------------------
        # CAMPOS OBLIGATORIOS
        # ----------------------------------------------------

        for campo in OBLIGATORIOS:

            if not p.get(campo):

                problemas.append(
                    f"Falta {campo}"
                )

        # ----------------------------------------------------
        # VALIDAR EMAIL
        # ----------------------------------------------------

        if (
            p["Email"]
            and not re.match(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                p["Email"]
            )
        ):

            problemas.append(
                f"Email con formato inválido: "
                f"'{p['Email']}'"
            )

        # ----------------------------------------------------
        # LONGITUDES
        # ----------------------------------------------------

        for campo, mx in MAX_LEN.items():

            if len(
                p.get(campo) or ""
            ) > mx:

                problemas.append(
                    f"{campo} supera "
                    f"{mx} caracteres"
                )

        # ----------------------------------------------------
        # CAMPOS OPCIONALES VACÍOS -> NULL
        # ----------------------------------------------------

        for campo in CAMPOS_TEXTO:

            if (
                p[campo] == ""
                and campo not in OBLIGATORIOS
            ):

                p[campo] = None

        filas.append({
            "fila": idx + 2,
            "payload": p,
            "problemas": problemas,
        })

    return filas


# ============================================================
# MAIN
# ============================================================

def main():

    ap = argparse.ArgumentParser()

    ap.add_argument(
        "excel",
        help="ruta del Excel a cargar"
    )

    ap.add_argument(
        "--hoja",
        default=0,
        help="hoja (nombre o índice; por defecto la primera)"
    )

    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="valida sin enviar nada"
    )

    ap.add_argument(
        "--limite",
        type=int,
        help="envía solo las primeras N filas válidas"
    )

    args = ap.parse_args()

    # --------------------------------------------------------
    # LEER EXCEL
    # --------------------------------------------------------

    df = pd.read_excel(
        args.excel,
        sheet_name=args.hoja,
        dtype=str
    )

    print(
        f"Excel leído: {len(df)} filas."
    )

    # --------------------------------------------------------
    # MAPEAR COLUMNAS
    # --------------------------------------------------------

    por_clave = {
        clave(c): c
        for c in df.columns
    }

    columnas = {}
    faltan = []

    for campo, encabezado in MAPA_COLUMNAS.items():

        col = por_clave.get(
            clave(encabezado)
        )

        if col is None:

            faltan.append(
                encabezado
            )

        else:

            columnas[campo] = col

    if faltan:

        sys.exit(
            "No encontré estas columnas "
            f"en el Excel: {faltan}\n"
            f"Columnas del archivo: {list(df.columns)}"
        )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    session = login()

    # --------------------------------------------------------
    # CÉLULAS
    # --------------------------------------------------------

    celulas_ids = cargar_celulas(
        session
    )

    if celulas_ids:

        print(
            "Células reconocidas:",
            {
                k: v
                for k, v in celulas_ids.items()
            }
        )

    # --------------------------------------------------------
    # CONSTRUIR FILAS
    # --------------------------------------------------------

    filas = construir_filas(
        df,
        columnas,
        celulas_ids
    )

    # --------------------------------------------------------
    # VALIDACIÓN
    #
    # IMPORTANTE:
    #
    # NO SE DEDUPLICA.
    #
    # No se rechaza:
    #   - Cédula repetida
    #   - Email repetido
    #   - Persona repetida
    #   - Célula repetida
    #
    # Cada fila válida del Excel se envía.
    # --------------------------------------------------------

    reporte = []
    pendientes = []

    # Se conservan estos diccionarios solamente
    # para compatibilidad con la estructura anterior.
    #
    # NO se utilizan para bloquear duplicados.
    vistos_ced = {}
    vistos_mail = {}

    for f in filas:

        p = f["payload"]

        base = {
            "fila": f["fila"],
            "cedula": p["Cedula"],
            "email": p["Email"],
            "nombre": (
                f"{p['Nombre']} "
                f"{p['Apellido']}"
            ).strip(),
        }

        # ----------------------------------------------------
        # FILA INVÁLIDA
        # ----------------------------------------------------

        if f["problemas"]:

            reporte.append({
                **base,
                "estado": "INVALIDO",
                "detalle": "; ".join(
                    f["problemas"]
                ),
            })

            continue

        # ----------------------------------------------------
        # NO HAY VALIDACIÓN DE DUPLICADOS
        # ----------------------------------------------------
        #
        # Antes existía:
        #
        # kc = clave(p["Cedula"])
        # km = p["Email"]
        #
        # if kc in vistos_ced or km in vistos_mail:
        #     ...
        #     continue
        #
        # Esa lógica está eliminada.
        #
        # Por lo tanto todas las filas válidas
        # pasan a pendientes.
        # ----------------------------------------------------

        kc = clave(
            p["Cedula"]
        )

        km = p["Email"]

        vistos_ced[kc] = f["fila"]
        vistos_mail[km] = f["fila"]

        pendientes.append(
            (f, base)
        )

    # --------------------------------------------------------
    # CONTADORES
    # --------------------------------------------------------

    n_dup = 0

    n_inv = sum(
        r["estado"] == "INVALIDO"
        for r in reporte
    )

    print(
        f"Válidas: {len(pendientes)} "
        f"| duplicadas: {n_dup} "
        f"| inválidas: {n_inv}"
    )

    # --------------------------------------------------------
    # LIMITE
    # --------------------------------------------------------

    if args.limite:

        pendientes = pendientes[
            :args.limite
        ]

        print(
            f"Se aplicó límite: "
            f"{len(pendientes)} registros."
        )

    # --------------------------------------------------------
    # DRY RUN
    # --------------------------------------------------------

    if args.dry_run:

        for f, base in pendientes:

            reporte.append({
                **base,
                "estado": "LISTO (dry-run)",
                "detalle": "",
            })

        print(
            "Dry-run: no se envió nada."
        )

    # --------------------------------------------------------
    # CARGA REAL
    # --------------------------------------------------------

    else:

        for i, (f, base) in enumerate(
            pendientes,
            1
        ):

            ok, status, detalle = enviar(
                session,
                f["payload"]
            )

            reporte.append({
                **base,
                "estado": (
                    "OK"
                    if ok
                    else "ERROR_API"
                ),
                "detalle": (
                    ""
                    if ok
                    else (
                        f"HTTP {status}: "
                        f"{detalle}"
                    )
                ),
            })

            if ok:

                print(
                    f"[{i}/{len(pendientes)}] "
                    f"fila {f['fila']}: OK"
                )

            else:

                print(
                    f"[{i}/{len(pendientes)}] "
                    f"fila {f['fila']}: "
                    f"ERROR {status}"
                )

            time.sleep(
                PAUSA_SEGUNDOS
            )

    # --------------------------------------------------------
    # ORDENAR REPORTE
    # --------------------------------------------------------

    reporte.sort(
        key=lambda r: r["fila"]
    )

    # --------------------------------------------------------
    # GUARDAR REPORTE
    # --------------------------------------------------------

    with open(
        "reporte_carga.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as fh:

        w = csv.DictWriter(
            fh,
            fieldnames=[
                "fila",
                "estado",
                "cedula",
                "email",
                "nombre",
                "detalle",
            ],
        )

        w.writeheader()

        w.writerows(
            reporte
        )

    print(
        "Reporte guardado en "
        "reporte_carga.csv"
    )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
```
