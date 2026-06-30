"""
Importa usuarios desde un Excel y los guarda en usuarios.json.

Columnas esperadas en el Excel:
  - correo  → nombre de usuario = texto antes de @
  - Celula  → célula asignada (obligatoria si rol es user/usuario)
  - rol     → admin o user

Uso:
  python crear_usuarios_excel.py
"""

import json
import os
import random

import bcrypt
import pandas as pd

# ── Configuración (misma carpeta que este script) ─────────────────────────────
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# 👉 Pon aquí el nombre de tu archivo Excel
EXCEL_FILE = os.path.join(CARPETA_SCRIPT, "usuarios.xlsx")

USUARIOS_FILE = os.path.join(CARPETA_SCRIPT, "usuarios.json")
ARCHIVO_SELECCION = os.path.join(CARPETA_SCRIPT, "data", "seleccion_proyectos.csv")
SALIDA_CREDENCIALES = os.path.join(CARPETA_SCRIPT, "usuarios_credenciales_generadas.csv")

# Contraseña numérica de 4 dígitos para todos (ej: "1234", "0000")
# Si lo dejas en None, se genera una clave distinta de 4 dígitos por usuario.
CLAVE_FIJA = "1234"

# Si True, actualiza usuarios que ya existan en usuarios.json
SOBRESCRIBIR_EXISTENTES = True

# Nombre de la hoja del Excel (None = primera hoja)
HOJA_EXCEL = None

# ── Columnas del Excel ────────────────────────────────────────────────────────
COL_CORREO = "correo"
COL_CELULA = "Celula"
COL_ROL = "rol"


def cargar_celulas_disponibles():
    if os.path.exists(ARCHIVO_SELECCION):
        df = pd.read_csv(ARCHIVO_SELECCION)
        return set(df["Celula"].dropna().astype(str).str.strip())
    return set()


def normalizar_columnas(df):
    mapa = {c.lower().strip(): c for c in df.columns}
    faltantes = []
    for esperada in (COL_CORREO, COL_CELULA, COL_ROL):
        if esperada.lower() not in mapa:
            faltantes.append(esperada)
    if faltantes:
        raise ValueError(
            f"Faltan columnas en el Excel: {', '.join(faltantes)}. "
            f"Columnas encontradas: {list(df.columns)}"
        )
    return df.rename(columns={
        mapa[COL_CORREO.lower()]: COL_CORREO,
        mapa[COL_CELULA.lower()]: COL_CELULA,
        mapa[COL_ROL.lower()]: COL_ROL,
    })


def usuario_desde_correo(correo):
    if pd.isna(correo) or not str(correo).strip():
        return None
    texto = str(correo).strip()
    if "@" not in texto:
        return texto.lower()
    return texto.split("@")[0].strip().lower()


def mapear_rol(rol_raw):
    if pd.isna(rol_raw):
        return None
    rol = str(rol_raw).strip().lower()
    if rol == "admin":
        return "admin"
    if rol in ("user", "usuario"):
        return "usuario"
    return None


def generar_clave():
    if CLAVE_FIJA is not None:
        return str(CLAVE_FIJA)
    return str(random.randint(1000, 9999))


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def guardar_usuarios(usuarios):
    with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


def celulas_de_registro(user):
    if user.get("celulas"):
        raw = user["celulas"]
        return list(raw) if isinstance(raw, list) else [raw]
    if user.get("celula"):
        raw = user["celula"]
        return list(raw) if isinstance(raw, list) else [raw]
    return []


def procesar_excel():
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ No se encontró el archivo Excel:\n   {EXCEL_FILE}")
        print("   Cambia la variable EXCEL_FILE al inicio del script.")
        return

    print(f"📂 Leyendo: {EXCEL_FILE}")
    df = pd.read_excel(EXCEL_FILE, sheet_name=HOJA_EXCEL or 0)
    df = normalizar_columnas(df)

    celulas_validas = cargar_celulas_disponibles()
    usuarios = cargar_usuarios()
    credenciales = []
    errores = []
    creados = 0
    actualizados = 0
    omitidos = 0

    # Agrupar filas por nombre de usuario (por si hay varias células para el mismo correo)
    filas_por_usuario = {}
    for idx, row in df.iterrows():
        nombre = usuario_desde_correo(row[COL_CORREO])
        if not nombre:
            errores.append(f"Fila {idx + 2}: correo vacío o inválido.")
            continue
        filas_por_usuario.setdefault(nombre, []).append(row)

    for nombre, filas in filas_por_usuario.items():
        roles = {mapear_rol(f[COL_ROL]) for f in filas}
        roles.discard(None)
        if not roles:
            errores.append(f"Usuario '{nombre}': rol inválido (usa admin o user).")
            continue
        if len(roles) > 1:
            errores.append(f"Usuario '{nombre}': roles contradictorios {roles}.")
            continue

        rol = roles.pop()
        celulas_fila = []
        for f in filas:
            cel = f[COL_CELULA]
            if pd.notna(cel) and str(cel).strip():
                celulas_fila.append(str(cel).strip())

        if rol == "usuario" and not celulas_fila:
            errores.append(f"Usuario '{nombre}': rol user requiere célula.")
            continue

        for cel in celulas_fila:
            if celulas_validas and cel not in celulas_validas:
                errores.append(f"Usuario '{nombre}': célula '{cel}' no está en seleccion_proyectos.csv.")

        if nombre in usuarios and not SOBRESCRIBIR_EXISTENTES:
            omitidos += 1
            continue

        clave = generar_clave()
        correo_ref = str(filas[0][COL_CORREO]).strip()

        datos = {
            "password": hash_password(clave),
            "rol": rol,
        }
        if rol == "usuario":
            # Unir células nuevas con las que ya tenía (sin duplicados)
            existentes = celulas_de_registro(usuarios.get(nombre, {}))
            datos["celulas"] = list(dict.fromkeys(existentes + celulas_fila))
            # Quitar formato antiguo si existía
            if "celula" in usuarios.get(nombre, {}):
                pass

        es_nuevo = nombre not in usuarios
        usuarios[nombre] = {**usuarios.get(nombre, {}), **datos}
        # Limpiar campo antiguo singular
        usuarios[nombre].pop("celula", None)

        credenciales.append({
            "usuario": nombre,
            "correo": correo_ref,
            "contraseña": clave,
            "rol": rol,
            "celulas": ", ".join(datos.get("celulas", [])),
        })

        if es_nuevo:
            creados += 1
        else:
            actualizados += 1

    if credenciales:
        guardar_usuarios(usuarios)
        pd.DataFrame(credenciales).to_csv(SALIDA_CREDENCIALES, index=False, encoding="utf-8-sig")

    print()
    print("─" * 50)
    print(f"✔️  Creados:      {creados}")
    print(f"🔄 Actualizados: {actualizados}")
    print(f"⏭️  Omitidos:     {omitidos}")
    print(f"❌ Errores:      {len(errores)}")
    if credenciales:
        print(f"📄 Credenciales: {SALIDA_CREDENCIALES}")
        print(f"💾 usuarios.json actualizado.")
    if CLAVE_FIJA is not None:
        print(f"🔑 Contraseña usada para todos: {CLAVE_FIJA}")

    if errores:
        print("\n⚠️  Detalle de errores / advertencias:")
        for e in errores:
            print(f"   - {e}")


if __name__ == "__main__":
    procesar_excel()
