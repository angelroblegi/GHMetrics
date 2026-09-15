"""
Comparador de asignación de proyectos a células entre dos archivos Excel.

Ejecutar:
    streamlit run comparar_celulas.py

Requisitos: streamlit, pandas, openpyxl
"""

import io
import re

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Comparador de Células", layout="wide")

COL_PROYECTO = "NombreProyecto"
COL_CELULA = "Celula"
SUFIJO_QUALITY = re.compile(r"\s*:\s*quality\s*$", flags=re.IGNORECASE)


# ---------------------------------------------------------------- utilidades


def normalizar_proyecto(valor, quitar_quality=True, ignorar_mayusculas=True):
    """Limpia el nombre del proyecto para poder cruzarlo entre archivos."""
    if pd.isna(valor):
        return ""
    texto = str(valor).strip()
    if quitar_quality:
        texto = SUFIJO_QUALITY.sub("", texto).strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto.casefold() if ignorar_mayusculas else texto


def normalizar_celula(valor, ignorar_mayusculas=True):
    if pd.isna(valor):
        return ""
    texto = re.sub(r"\s+", " ", str(valor).strip())
    return texto.casefold() if ignorar_mayusculas else texto


@st.cache_data(show_spinner=False)
def leer_excel(contenido: bytes):
    """Devuelve un dict {nombre_hoja: DataFrame}."""
    return pd.read_excel(io.BytesIO(contenido), sheet_name=None, dtype=str)


def preparar(df, col_proyecto, col_celula, quitar_quality, ignorar_mayusculas, origen):
    """Deja un DataFrame con las claves normalizadas y el valor original."""
    base = df[[col_proyecto, col_celula]].copy()
    base.columns = ["proyecto_original", "celula_original"]
    base["proyecto_original"] = base["proyecto_original"].fillna("").astype(str).str.strip()
    base["celula_original"] = base["celula_original"].fillna("").astype(str).str.strip()
    base = base[base["proyecto_original"] != ""]

    base["clave"] = base["proyecto_original"].map(
        lambda v: normalizar_proyecto(v, quitar_quality, ignorar_mayusculas)
    )
    base["celula_key"] = base["celula_original"].map(
        lambda v: normalizar_celula(v, ignorar_mayusculas)
    )
    base["origen"] = origen
    return base[base["clave"] != ""]


def colapsar(base):
    """Un registro por clave. Si hay duplicados, concatena las células distintas."""
    agrupado = (
        base.groupby("clave", as_index=False)
        .agg(
            proyecto=("proyecto_original", "first"),
            celula=("celula_original", lambda s: " | ".join(sorted(set(s)))),
            celula_key=("celula_key", lambda s: " | ".join(sorted(set(s)))),
            repeticiones=("proyecto_original", "size"),
        )
    )
    return agrupado


def a_excel(hojas: dict) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for nombre, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre[:31], index=False)
    return buffer.getvalue()


def selector_columnas(df, etiqueta, key):
    columnas = list(df.columns)
    idx_proy = columnas.index(COL_PROYECTO) if COL_PROYECTO in columnas else 0
    idx_cel = columnas.index(COL_CELULA) if COL_CELULA in columnas else min(1, len(columnas) - 1)
    c1, c2 = st.columns(2)
    with c1:
        col_proy = st.selectbox(f"Columna de proyecto ({etiqueta})", columnas, index=idx_proy, key=f"{key}_p")
    with c2:
        col_cel = st.selectbox(f"Columna de célula ({etiqueta})", columnas, index=idx_cel, key=f"{key}_c")
    return col_proy, col_cel


# ------------------------------------------------------------------- sidebar

st.title("Comparador de proyectos por célula")
st.caption("Carga dos Excel con NombreProyecto y Celula para ver qué cambió entre ellos.")

with st.sidebar:
    st.header("Opciones de comparación")
    quitar_quality = st.checkbox(
        "Ignorar el sufijo ':Quality'", value=True,
        help="Trata 'MiProyecto:Quality' y 'MiProyecto' como el mismo componente.",
    )
    ignorar_mayusculas = st.checkbox("Ignorar mayúsculas y tildes de espaciado", value=True)
    nombre_a = st.text_input("Etiqueta archivo A", value="Archivo A")
    nombre_b = st.text_input("Etiqueta archivo B", value="Archivo B")

col_izq, col_der = st.columns(2)
with col_izq:
    archivo_a = st.file_uploader(f"{nombre_a} (.xlsx)", type=["xlsx", "xlsm", "xls"], key="fa")
with col_der:
    archivo_b = st.file_uploader(f"{nombre_b} (.xlsx)", type=["xlsx", "xlsm", "xls"], key="fb")

if not archivo_a or not archivo_b:
    st.info("Sube los dos archivos para comenzar.")
    st.stop()

hojas_a = leer_excel(archivo_a.getvalue())
hojas_b = leer_excel(archivo_b.getvalue())

with col_izq:
    hoja_a = st.selectbox(f"Hoja ({nombre_a})", list(hojas_a.keys()), key="ha")
    df_a = hojas_a[hoja_a]
    col_proy_a, col_cel_a = selector_columnas(df_a, nombre_a, "a")

with col_der:
    hoja_b = st.selectbox(f"Hoja ({nombre_b})", list(hojas_b.keys()), key="hb")
    df_b = hojas_b[hoja_b]
    col_proy_b, col_cel_b = selector_columnas(df_b, nombre_b, "b")

# ---------------------------------------------------------------- comparación

base_a = preparar(df_a, col_proy_a, col_cel_a, quitar_quality, ignorar_mayusculas, nombre_a)
base_b = preparar(df_b, col_proy_b, col_cel_b, quitar_quality, ignorar_mayusculas, nombre_b)

dup_a = base_a[base_a.duplicated("clave", keep=False)]
dup_b = base_b[base_b.duplicated("clave", keep=False)]

ag_a = colapsar(base_a)
ag_b = colapsar(base_b)

cruce = ag_a.merge(ag_b, on="clave", how="outer", suffixes=("_a", "_b"), indicator=True)

solo_a = cruce[cruce["_merge"] == "left_only"][["proyecto_a", "celula_a"]].rename(
    columns={"proyecto_a": "Proyecto", "celula_a": f"Célula en {nombre_a}"}
)
solo_b = cruce[cruce["_merge"] == "right_only"][["proyecto_b", "celula_b"]].rename(
    columns={"proyecto_b": "Proyecto", "celula_b": f"Célula en {nombre_b}"}
)

ambos = cruce[cruce["_merge"] == "both"].copy()
ambos["cambio"] = ambos["celula_key_a"] != ambos["celula_key_b"]

diferentes = ambos[ambos["cambio"]][["proyecto_a", "celula_a", "celula_b"]].rename(
    columns={
        "proyecto_a": "Proyecto",
        "celula_a": f"Célula en {nombre_a}",
        "celula_b": f"Célula en {nombre_b}",
    }
)
iguales = ambos[~ambos["cambio"]][["proyecto_a", "celula_a"]].rename(
    columns={"proyecto_a": "Proyecto", "celula_a": "Célula"}
)

for df in (solo_a, solo_b, diferentes, iguales):
    df.sort_values(df.columns[0], inplace=True, key=lambda s: s.str.casefold())
    df.reset_index(drop=True, inplace=True)

# ------------------------------------------------------------------ resultados

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric(f"Proyectos {nombre_a}", len(ag_a))
m2.metric(f"Proyectos {nombre_b}", len(ag_b))
m3.metric("Célula distinta", len(diferentes))
m4.metric(f"Solo en {nombre_a}", len(solo_a))
m5.metric(f"Solo en {nombre_b}", len(solo_b))

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        f"Célula distinta ({len(diferentes)})",
        f"Solo en {nombre_a} ({len(solo_a)})",
        f"Solo en {nombre_b} ({len(solo_b)})",
        f"Sin cambios ({len(iguales)})",
    ]
)

with tab1:
    st.subheader("Proyectos asignados a células diferentes")
    if diferentes.empty:
        st.success("Ningún proyecto cambió de célula.")
    else:
        filtro = st.text_input("Filtrar por texto", key="f1")
        vista = diferentes
        if filtro:
            mascara = vista.apply(
                lambda fila: filtro.casefold() in " ".join(fila.astype(str)).casefold(), axis=1
            )
            vista = vista[mascara]
        st.dataframe(vista, use_container_width=True, hide_index=True)

with tab2:
    st.dataframe(solo_a, use_container_width=True, hide_index=True)

with tab3:
    st.dataframe(solo_b, use_container_width=True, hide_index=True)

with tab4:
    st.dataframe(iguales, use_container_width=True, hide_index=True)

# --------------------------------------------------------------- advertencias

if not dup_a.empty or not dup_b.empty:
    with st.expander("Proyectos duplicados detectados"):
        st.caption(
            "Se agruparon en un solo registro; si tenían células distintas quedan "
            "concatenadas con ' | '."
        )
        if not dup_a.empty:
            st.write(f"**{nombre_a}**")
            st.dataframe(
                dup_a[["proyecto_original", "celula_original"]].rename(
                    columns={"proyecto_original": "Proyecto", "celula_original": "Célula"}
                ),
                use_container_width=True,
                hide_index=True,
            )
        if not dup_b.empty:
            st.write(f"**{nombre_b}**")
            st.dataframe(
                dup_b[["proyecto_original", "celula_original"]].rename(
                    columns={"proyecto_original": "Proyecto", "celula_original": "Célula"}
                ),
                use_container_width=True,
                hide_index=True,
            )

# ------------------------------------------------------------------ descarga

st.divider()
st.download_button(
    "Descargar comparación en Excel",
    data=a_excel(
        {
            "Celula distinta": diferentes,
            f"Solo {nombre_a}": solo_a,
            f"Solo {nombre_b}": solo_b,
            "Sin cambios": iguales,
        }
    ),
    file_name="comparacion_celulas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
