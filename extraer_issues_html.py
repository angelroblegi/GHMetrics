#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT 1 - PRUEBA
Inserta UNA persona ficticia en el CommanCenter API y lista las células existentes.

Requisitos:  pip install requests
Uso:         python prueba_consultor.py

Credenciales: variables de entorno API_USER y API_PASSWORD, o el script las pide.
"""
import getpass
import os
import sys

import requests

# ══════════════════════ CONFIGURACIÓN (ajusta esto) ══════════════════════
API_URL = os.getenv("API_URL", "https://localhost:65002")  # sin "/" al final
LOGIN_PATH = "/api/auth/login"          # <- ajustar a tu AuthController
LOGIN_USER_FIELD = "usuario"              # campo de usuario en el DTO de login
LOGIN_PASS_FIELD = "password"           # campo de contraseña en el DTO de login
CONSULTORES_PATH = "/api/consultores"   # <- ajustar a tu ConsultoresController (POST)
CELULAS_PATH = "/api/celulas"           # <- GET que lista las células

# Id de una célula existente. Si lo dejas en None, usa la primera que encuentre.
CELULA_ID_PRUEBA = None
# ═════════════════════════════════════════════════════════════════════════

PERSONA_PRUEBA = {
    #aqui iban datos
}


def buscar_token(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ("token", "accesstoken", "access_token", "jwt") and isinstance(v, str):
                return v
        for v in obj.values():
            t = buscar_token(v)
            if t:
                return t
    return None


def login():
    user = os.getenv("API_USER") or input("Usuario del API: ").strip()
    pwd = os.getenv("API_PASSWORD") or input("Contraseña del API: ").strip()
    r = requests.post(API_URL + LOGIN_PATH,
                      json={LOGIN_USER_FIELD: user, LOGIN_PASS_FIELD: pwd}, timeout=60, verify=False)
    if r.status_code >= 300:
        sys.exit(f"Login falló ({r.status_code}): {r.text[:300]}")
    token = buscar_token(r.json())
    if not token:
        sys.exit(f"No encontré el token en la respuesta del login: {r.text[:300]}")
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {token}"
    print("Login correcto.")
    return s


def listar_celulas(session):
    """Devuelve lista de (id, nombre) leída del API; vacía si no se pudo."""
    try:
        r = session.get(API_URL + CELULAS_PATH, timeout=60, verify=False)
        data = r.json() if r.status_code < 300 else []
        if isinstance(data, dict):
            data = next((v for v in data.values() if isinstance(v, list)), [])
        out = []
        for it in data:
            low = {k.lower(): v for k, v in it.items()}
            if "id" in low and "nombre" in low:
                out.append((low["id"], low["nombre"]))
        return out
    except Exception as e:  # noqa: BLE001
        print(f"Aviso: no pude leer las células ({e}).")
        return []


def main():
    s = login()
    celulas = listar_celulas(s)
    if celulas:
        print("Células disponibles:")
        for cid, nombre in celulas:
            print(f"  {cid}: {nombre}")
    else:
        print("No pude listar células; define CELULA_ID_PRUEBA a mano.")

    celula_id = CELULA_ID_PRUEBA if CELULA_ID_PRUEBA is not None else (celulas[0][0] if celulas else None)
    if celula_id is None:
        sys.exit("No hay célula para asignar. Define CELULA_ID_PRUEBA.")

    payload = dict(PERSONA_PRUEBA)
    payload["Celulas"] = [{"CelulaId": celula_id, "PorcentajeParticipacion": None}]

    r = s.post(API_URL + CONSULTORES_PATH, json=payload, timeout=60)
    ok = r.status_code < 300
    print(f"\nResultado: {'OK' if ok else 'ERROR'} (HTTP {r.status_code})\n{r.text[:500]}")
    if ok:
        print("\nQuedó creado 'prueba.carga@example.com'. El email es único: "
              "deshabilítalo o bórralo antes de repetir la prueba.")


if __name__ == "__main__":
    main()
