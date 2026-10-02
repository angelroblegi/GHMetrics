import requests
import urllib3

urllib3.disable_warnings()

SONAR_URL = "https://TU_SONAR"
TOKEN = "squ_TU_TOKEN"
PROJECT_KEY = "CLAVE_DEL_PROYECTO"
BRANCH = "main"

r = requests.post(
    f"{SONAR_URL}/api/project_branches/set_main",
    params={"project": PROJECT_KEY, "branch": BRANCH},
    auth=(TOKEN, ""),
    verify=False,
)
print(r.status_code, r.text)

r = requests.get(
    f"{SONAR_URL}/api/project_branches/list",
    params={"project": PROJECT_KEY},
    auth=(TOKEN, ""),
    verify=False,
)
for b in r.json().get("branches", []):
    print(b["name"], "-> principal" if b.get("isMain") else "")
