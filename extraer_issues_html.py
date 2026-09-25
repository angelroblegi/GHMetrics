import requests
import pandas as pd

# --- Configuración ---
SONAR_URL = "https://tu-sonarqube.com"   # <-- ajusta, sin / al final
TOKEN = "TU_TOKEN"                        # <-- ajusta
EXCEL_PATH = "proyectos_tags.xlsx"        # <-- ajusta


def set_tag(project_key: str, tag: str):
    url = f"{SONAR_URL}/api/project_tags/set"
    resp = requests.post(
        url,
        auth=(TOKEN, ""),
        data={"project": project_key, "tags": tag},
        verify=False,  # corporate proxy
    )
    return resp


def get_all_projects():
    """Trae todos los proyectos de la instancia (paginado)."""
    projects = []
    page = 1
    page_size = 500
    while True:
        url = f"{SONAR_URL}/api/projects/search"
        resp = requests.get(
            url,
            auth=(TOKEN, ""),
            params={"p": page, "ps": page_size},
            verify=False,
        )
        resp.raise_for_status()
        data = resp.json()
        projects.extend(data["components"])
        total = data["paging"]["total"]
        if page * page_size >= total:
            break
        page += 1
    return projects  # cada item trae al menos "key" y "name"


def get_project_tags(project_key: str):
    """Trae los tags actuales de un proyecto puntual."""
    url = f"{SONAR_URL}/api/navigation/component"
    resp = requests.get(
        url,
        auth=(TOKEN, ""),
        params={"component": project_key},
        verify=False,
    )
    if resp.status_code != 200:
        return []
    return resp.json().get("tags", [])


def main():
    df = pd.read_excel(EXCEL_PATH)
    df.columns = [c.strip() for c in df.columns]

    if "NombreProyecto" not in df.columns or "Celula" not in df.columns:
        raise ValueError("El Excel debe tener las columnas 'NombreProyecto' y 'Celula'")

    resultados = []

    for _, row in df.iterrows():
        project_key = str(row["NombreProyecto"]).strip()
        tag = str(row["Celula"]).strip()

        if not project_key or project_key == "nan" or not tag or tag == "nan":
            continue

        resp = set_tag(project_key, tag)
        estado = "OK" if resp.status_code == 204 else f"ERROR {resp.status_code}: {resp.text}"

        print(f"{project_key} -> tag '{tag}': {estado}")
        resultados.append({"project_key": project_key, "tag": tag, "estado": estado})

    pd.DataFrame(resultados).to_excel("resultado_tags.xlsx", index=False)

    # --- Verificación final: proyectos en Sonar sin ningún tag ---
    print("\nRevisando proyectos sin tag en toda la instancia de Sonar...")
    todos_los_proyectos = get_all_projects()
    sin_tag = []

    for proj in todos_los_proyectos:
        key = proj["key"]
        name = proj.get("name", "")
        tags = get_project_tags(key)
        if not tags:
            sin_tag.append({"project_key": key, "name": name})

    if sin_tag:
        print(f"\n⚠️  Hay {len(sin_tag)} proyectos en Sonar SIN ningún tag:")
        for p in sin_tag:
            print(f"   - {p['project_key']} ({p['name']})")
        pd.DataFrame(sin_tag).to_excel("proyectos_sin_tag.xlsx", index=False)
        print("\nDetalle guardado en proyectos_sin_tag.xlsx")
    else:
        print("\n✅ Todos los proyectos de la instancia tienen al menos un tag.")

    print("\nProceso terminado. Ver resultado_tags.xlsx para el detalle de la asignación.")


if __name__ == "__main__":
    main()
