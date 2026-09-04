"""
Extrae, para cada proyecto listado en un Excel, los componentes (archivos)
que tienen issues ACTIVOS relacionados con reglas HTML en SonarQube, y genera
un Excel de salida con el detalle y un resumen por célula.

Requisitos:
    pip install requests pandas openpyxl

Uso:
    python extraer_issues_html.py
    (el script te pedirá la ruta del Excel de entrada al ejecutarse)
"""

import requests
import pandas as pd
import urllib3
from datetime import datetime

# Desactiva warnings de certificado SSL (proxy corporativo AEL)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# CONFIGURACIÓN - COMPLETA AQUÍ TUS DATOS
# ============================================================
SONAR_URL = ""      # <-- Ej: "https://sonarqube.tuempresa.com"
SONAR_TOKEN = ""    # <-- Tu token de acceso de SonarQube

# Nombre de la columna en el Excel de entrada que contiene el project key
COL_PROYECTO = "NombreProyecto"

# Nombre de la columna de célula en el Excel de entrada (si existe).
# Si tu archivo no tiene esta columna, déjalo igual: el script lo detecta
# automáticamente y llena "Sin Célula" en su lugar.
COL_CELULA = "Celula"

# Filtro de reglas HTML en SonarQube.
# El plugin HTML de SonarQube usa el "language key" = "web" y el
# repositorio de reglas "Web" (reglas tipo Web:S1234). Se usa el filtro
# de lenguaje, que es el más confiable.
SONAR_LANGUAGE_FILTER = "web"

# Solo issues activos (no resueltos)
SONAR_RESOLVED = "false"

# Tamaño de página para la API de SonarQube (máx. 500)
PAGE_SIZE = 500

# ============================================================
# FIN CONFIGURACIÓN
# ============================================================


def pedir_archivo_entrada() -> str:
    ruta = input(
        "Ingresa la ruta/nombre del archivo Excel de entrada "
        f"(debe tener una columna llamada '{COL_PROYECTO}'): "
    ).strip()
    return ruta.strip('"').strip("'")


def cargar_proyectos(ruta_excel: str) -> pd.DataFrame:
    df = pd.read_excel(ruta_excel)

    if COL_PROYECTO not in df.columns:
        raise ValueError(
            f"El archivo no tiene una columna llamada '{COL_PROYECTO}'. "
            f"Columnas encontradas: {list(df.columns)}"
        )

    tiene_celula = COL_CELULA in df.columns
    if not tiene_celula:
        print(
            f"Aviso: no se encontró la columna '{COL_CELULA}' en el archivo. "
            "Se usará 'Sin Célula' para todos los proyectos."
        )
        df[COL_CELULA] = "Sin Célula"

    df = df[[COL_PROYECTO, COL_CELULA]].dropna(subset=[COL_PROYECTO])
    df[COL_PROYECTO] = df[COL_PROYECTO].astype(str).str.strip()
    df[COL_CELULA] = df[COL_CELULA].fillna("Sin Célula")
    df = df.drop_duplicates(subset=[COL_PROYECTO])
    return df


def obtener_issues_html(project_key: str) -> list:
    """Trae todos los issues activos de reglas HTML para un proyecto,
    paginando la API de SonarQube."""
    issues = []
    page = 1

    while True:
        params = {
            "componentKeys": project_key,
            "languages": SONAR_LANGUAGE_FILTER,
            "resolved": SONAR_RESOLVED,
            "ps": PAGE_SIZE,
            "p": page,
        }
        resp = requests.get(
            f"{SONAR_URL}/api/issues/search",
            params=params,
            auth=(SONAR_TOKEN, ""),
            verify=False,
            timeout=60,
        )

        if resp.status_code != 200:
            print(
                f"  [ERROR] {project_key}: HTTP {resp.status_code} - {resp.text[:200]}"
            )
            break

        data = resp.json()
        issues.extend(data.get("issues", []))

        total = data.get("total", 0)
        if page * PAGE_SIZE >= total:
            break
        page += 1

    return issues


def procesar(df_proyectos: pd.DataFrame) -> pd.DataFrame:
    filas = []

    for _, row in df_proyectos.iterrows():
        proyecto = row[COL_PROYECTO]
        celula = row[COL_CELULA]

        print(f"Consultando: {proyecto} ...")
        issues = obtener_issues_html(proyecto)
        print(f"  -> {len(issues)} issue(s) HTML activo(s)")

        for issue in issues:
            componente_completo = issue.get("component", "")
            # El componente viene como "projectKey:ruta/archivo.html"
            archivo = (
                componente_completo.split(":", 1)[1]
                if ":" in componente_completo
                else componente_completo
            )

            filas.append(
                {
                    "Célula": celula,
                    "Proyecto": proyecto,
                    "Componente": componente_completo,
                    "Archivo": archivo,
                    "Regla": issue.get("rule", ""),
                    "Severidad": issue.get("severity", ""),
                    "Tipo": issue.get("type", ""),
                    "Mensaje": issue.get("message", ""),
                    "Línea": issue.get("line", ""),
                    "Estado": issue.get("status", ""),
                    "Fecha Creación": issue.get("creationDate", ""),
                    "Issue Key": issue.get("key", ""),
                }
            )

    return pd.DataFrame(filas)


def generar_excel_salida(df_detalle: pd.DataFrame) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_salida = f"issues_html_por_componente_{timestamp}.xlsx"

    with pd.ExcelWriter(nombre_salida, engine="openpyxl") as writer:
        if df_detalle.empty:
            pd.DataFrame(
                [{"Info": "No se encontraron issues activos de reglas HTML."}]
            ).to_excel(writer, sheet_name="Detalle", index=False)
        else:
            df_detalle.to_excel(writer, sheet_name="Detalle", index=False)

            # Resumen por célula
            resumen_celula = (
                df_detalle.groupby("Célula")
                .agg(
                    Proyectos_Afectados=("Proyecto", "nunique"),
                    Componentes_Afectados=("Componente", "nunique"),
                    Total_Issues=("Issue Key", "count"),
                )
                .reset_index()
                .sort_values("Total_Issues", ascending=False)
            )
            resumen_celula.to_excel(writer, sheet_name="Resumen por Célula", index=False)

            # Resumen por componente
            resumen_componente = (
                df_detalle.groupby(["Célula", "Proyecto", "Componente"])
                .agg(Total_Issues=("Issue Key", "count"))
                .reset_index()
                .sort_values("Total_Issues", ascending=False)
            )
            resumen_componente.to_excel(
                writer, sheet_name="Resumen por Componente", index=False
            )

    return nombre_salida


def main():
    if not SONAR_URL or not SONAR_TOKEN:
        print(
            "Falta configurar SONAR_URL y/o SONAR_TOKEN al inicio del script. "
            "Complétalos y vuelve a ejecutar."
        )
        return

    ruta_entrada = pedir_archivo_entrada()
    df_proyectos = cargar_proyectos(ruta_entrada)
    print(f"\n{len(df_proyectos)} proyecto(s) cargado(s) desde el Excel.\n")

    df_detalle = procesar(df_proyectos)
    archivo_salida = generar_excel_salida(df_detalle)

    print(f"\nListo. Archivo generado: {archivo_salida}")
    print(f"Total de issues HTML activos encontrados: {len(df_detalle)}")


if __name__ == "__main__":
    main()
