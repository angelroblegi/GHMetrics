import requests

# --- Configuración: edita estos valores ---
SONAR_URL = "https://tu-sonarqube.com"   # <-- ajusta, sin / al final
TOKEN = "TU_TOKEN"                        # <-- ajusta
PROJECT_KEY = "mi-proyecto-key"           # <-- ajusta
TAG = "Transformacion-Digital"            # <-- ajusta (la célula)


def set_tag(project_key: str, tag: str):
    url = f"{SONAR_URL}/api/project_tags/set"
    resp = requests.post(
        url,
        auth=(TOKEN, ""),
        data={"project": project_key, "tags": tag},
        verify=False,  # corporate proxy
    )
    return resp


def get_project_tags(project_key: str):
    url = f"{SONAR_URL}/api/navigation/component"
    resp = requests.get(
        url,
        auth=(TOKEN, ""),
        params={"component": project_key},
        verify=False,
    )
    resp.raise_for_status()
    return resp.json().get("tags", [])


if __name__ == "__main__":
    print(f"Asignando tag '{TAG}' al proyecto '{PROJECT_KEY}'...")
    resp = set_tag(PROJECT_KEY, TAG)

    if resp.status_code == 204:
        print("✅ Asignación exitosa (204 No Content)")
    else:
        print(f"❌ Error {resp.status_code}: {resp.text}")

    print("\nVerificando tags actuales del proyecto...")
    tags = get_project_tags(PROJECT_KEY)
    print(f"Tags actuales de '{PROJECT_KEY}': {tags}")
