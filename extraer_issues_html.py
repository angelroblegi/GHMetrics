import requests
import pandas as pd

# --- Configuración ---
SONAR_URL = "https://tu-sonarqube.com"   # <-- ajusta, sin / al final
TOKEN = "TU_TOKEN"                        # <-- ajusta
EXCEL_PATH = "proyectos_tags.xlsx"        # <-- ajusta

# --- Entradas manuales adicionales (key, tag) ---
# Aquí pegas los keys que me vayas a pasar en el chat, junto con su célula/tag
MANUAL_ENTRIES = [
    # ("key-del-proyecto-1", "Celula-1"),
    # ("key-del-proyecto-2", "Celula-2"),
]


def get_project_tags(project_key: str):
    url = f"{SONAR_URL}/api/navigation/component"
    resp = requests.get(url, auth=(TOKEN, ""), params={"component": project_key}, verify=False)
    if resp.status_code != 200:
        return None
    return resp.json().get("tags", [])


def set_tags(project_key: str, tags: list):
    url = f"{SONAR_URL}/api/project_tags/set"
    resp = requests.post(
        url, auth=(TOKEN, ""),
        data={"project": project_key, "tags": ",".join(tags)},
        verify=False,
    )
    return resp


def get_all_projects():
    """Trae todos los proyectos de la instancia (paginado)."""
    projects = []
    page = 1
    page_size = 500
    while True:
        url = f"{SONAR_URL}/api/projects/search"
        resp = requests.get(url, auth=(TOKEN, ""), params={"p": page, "ps": page_size}, verify=False)
        resp.raise_for_status()
        data = resp.json()
        projects.extend(data["components"])
        if page * page_size >= data["paging"]["total"]:
            break
        page += 1
    return projects


def procesar(project_key: str, tag: str, resultados: list, fallos: list, origen: str):
    tags_actuales = get_project_tags(project_key)

    if tags_actuales is None:
        msg = "No se pudo consultar el proyecto (key inválida o error de API)"
        print(f"❌ [{origen}] {project_key}: {msg}")
        fallos.append({"key": project_key, "tag": tag, "origen": origen, "motivo": msg})
        return

    if tag in tags_actuales:
        print(f"✔️  [{origen}] {project_key}: ya tenía el tag '{tag}', sin cambios")
        resultados.append({"key": project_key, "tag": tag, "origen": origen, "estado": "YA_EXISTIA"})
        return

    nuevos_tags = tags_actuales + [tag]
    resp = set_tags(project_key, nuevos_tags)

    if resp.status_code == 204:
        print(f"✅ [{origen}] {project_key}: tag '{tag}' asignado. Tags finales: {nuevos_tags}")
        resultados.append({"key": project_key, "tag": tag, "origen": origen, "estado": "OK"})
    else:
        msg = f"Error {resp.status_code}: {resp.text}"
        print(f"❌ [{origen}] {project_key}: {msg}")
        fallos.append({"key": project_key, "tag": tag, "origen": origen, "motivo": msg})


def main():
    resultados = []
    fallos = []

    print("=== Procesando proyectos del Excel ===\n")
    df = pd.read_excel(EXCEL_PATH)
    df.columns = [c.strip() for c in df.columns]

    if "NombreProyecto" not in df.columns or "Celula" not in df.columns:
        raise ValueError("El Excel debe tener las columnas 'NombreProyecto' y 'Celula'")

    for _, row in df.iterrows():
        key = str(row["NombreProyecto"]).strip()
        tag = str(row["Celula"]).strip()
        if not key or key == "nan" or not tag or tag == "nan":
            continue
        procesar(key, tag, resultados, fallos, origen="Excel")

    print("\n=== Procesando entradas manuales ===\n")
    if not MANUAL_ENTRIES:
        print("(No hay entradas manuales cargadas)")
    for key, tag in MANUAL_ENTRIES:
        procesar(key.strip(), tag.strip(), resultados, fallos, origen="Manual")

    # --- Resumen de fallos ---
    print("\n=== Resumen ===")
    if fallos:
        print(f"⚠️  {len(fallos)} entradas fallaron:")
        for f in fallos:
            print(f"   - [{f['origen']}] {f['key']} / {f['tag']}: {f['motivo']}")
    else:
        print("✅ Ninguna entrada falló.")

    pd.DataFrame(resultados).to_excel("resultado_tags.xlsx", index=False)
    if fallos:
        pd.DataFrame(fallos).to_excel("fallos_tags.xlsx", index=False)

    # --- Verificación final: proyectos en toda la instancia sin ningún tag ---
    print("\n=== Revisando proyectos sin tag en toda la instancia ===")
    todos_los_proyectos = get_all_projects()
    sin_tag = []

    for proj in todos_los_proyectos:
        key = proj["key"]
        name = proj.get("name", "")
        tags = get_project_tags(key)
        if not tags:
            sin_tag.append({"project_key": key, "name": name})

    if sin_tag:
        print(f"⚠️  {len(sin_tag)} proyectos en Sonar SIN ningún tag:")
        for p in sin_tag:
            print(f"   - {p['project_key']} ({p['name']})")
        pd.DataFrame(sin_tag).to_excel("proyectos_sin_tag.xlsx", index=False)
        print("\nDetalle guardado en proyectos_sin_tag.xlsx")
    else:
        print("✅ Todos los proyectos de la instancia tienen al menos un tag.")

    print(f"\nProceso terminado. Resultados: resultado_tags.xlsx" + (" | Fallos: fallos_tags.xlsx" if fallos else ""))


if __name__ == "__main__":
    main()
