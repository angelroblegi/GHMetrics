#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SCRIPT - PRUEBA DE CREACIÓN DE CONSULTOR

Inserta UNA persona ficticia en el CommanCenter API
y lista las células existentes.

Requisitos:
    pip install requests

Uso:
    python cargue_prueba.py

Credenciales:
    Variables de entorno API_USER y API_PASSWORD,
    o el script las solicita por consola.
"""

import getpass
import os
import sys

import requests
import urllib3


# ============================================================
# CONFIGURACIÓN
# ============================================================

# URL de tu API local
API_URL = os.getenv(
    "API_URL",
    "https://localhost:65002"
)

# Endpoint de autenticación
LOGIN_PATH = "/api/auth/login"

# Campos definidos en LoginDto
LOGIN_USER_FIELD = "usuario"
LOGIN_PASS_FIELD = "password"

# Endpoint para crear consultores
CONSULTORES_PATH = "/api/consultores"

# Endpoint para consultar células
CELULAS_PATH = "/api/celulas"

# Si quieres especificar manualmente una célula:
# CELULA_ID_PRUEBA = 1
#
# Si lo dejas en None, el script utilizará
# automáticamente la primera célula encontrada.
CELULA_ID_PRUEBA = None


# ============================================================
# CERTIFICADO SSL LOCAL
# ============================================================

# Estamos trabajando con localhost y un certificado
# autofirmado de ASP.NET Core.
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)


# ============================================================
# DATOS DEL CONSULTOR DE PRUEBA
# ============================================================

PERSONA_PRUEBA = {
    "Cedula": "PRUEBA-0001",
    "Nombre": "Prueba",
    "Apellido": "Carga",
    "Email": "prueba.carga@example.com",
    "Celular": "3000000000",
    "Cargo": "Consultor de prueba",
    "Rol": "Prueba",
    "Empresa": "Prueba",
    "Ciudad": "Bogotá",
    "Direccion": "Calle 1 # 2-3",
    "Barrio": "Centro",
    "ContactoEmergenciaNombre": "Contacto Prueba",
    "ContactoEmergenciaTelefono": "3000000001",
    "Estado": "Activo",

    # CrearConsultorDto exige estas dos fechas
    "FechaIngreso": "2024-01-15T00:00:00",
    "FechaNacimiento": "1990-01-15T00:00:00",

    "Observaciones": "Registro creado para prueba de API",
    "FotoUrl": None
}


# ============================================================
# BUSCAR TOKEN
# ============================================================

def buscar_token(obj):
    """
    Busca recursivamente AccessToken/Token/JWT
    dentro de la respuesta JSON.
    """

    if isinstance(obj, dict):

        for key, value in obj.items():

            if (
                key.lower()
                in ("token", "accesstoken", "access_token", "jwt")
                and isinstance(value, str)
            ):
                return value

        for value in obj.values():

            token = buscar_token(value)

            if token:
                return token

    return None


# ============================================================
# LOGIN
# ============================================================

def login():

    user = (
        os.getenv("API_USER")
        or input("Usuario del API: ").strip()
    )

    pwd = (
        os.getenv("API_PASSWORD")
        or getpass.getpass("Contraseña del API: ")
    )

    login_payload = {
        LOGIN_USER_FIELD: user,
        LOGIN_PASS_FIELD: pwd
    }

    print("\nConectando al API...")
    print(f"URL: {API_URL + LOGIN_PATH}")

    try:

        response = requests.post(
            API_URL + LOGIN_PATH,
            json=login_payload,
            timeout=60,
            verify=False
        )

    except requests.exceptions.RequestException as e:

        sys.exit(
            f"\nError conectando con el API durante el login:\n{e}"
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
            "\nEl login respondió correctamente, "
            "pero la respuesta no es JSON:\n"
            f"{response.text[:500]}"
        )

    token = buscar_token(data)

    if not token:

        sys.exit(
            "\nNo encontré el AccessToken en la respuesta del login:\n"
            f"{response.text[:500]}"
        )

    session = requests.Session()

    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    })

    # Deshabilitar validación SSL para localhost
    session.verify = False

    print("Login correcto.")

    return session


# ============================================================
# LISTAR CÉLULAS
# ============================================================

def listar_celulas(session):

    print("\nConsultando células...")
    print(f"URL: {API_URL + CELULAS_PATH}")

    try:

        response = session.get(
            API_URL + CELULAS_PATH,
            timeout=60
        )

        print(
            f"Respuesta células: HTTP {response.status_code}"
        )

        if response.status_code >= 300:

            print(
                "No fue posible obtener las células.\n"
                f"Respuesta:\n{response.text[:500]}"
            )

            return []

        data = response.json()

    except requests.exceptions.RequestException as e:

        print(
            "\nError conectando con el endpoint de células:"
        )

        print(e)

        return []

    except ValueError:

        print(
            "\nLa respuesta de células no es JSON válido:"
        )

        print(response.text[:500])

        return []

    # ========================================================
    # Procesar respuesta
    # ========================================================

    if isinstance(data, dict):

        # Algunos endpoints devuelven:
        #
        # {
        #     "data": [...]
        # }
        #
        # o:
        #
        # {
        #     "items": [...]
        # }

        data = next(
            (
                value
                for value in data.values()
                if isinstance(value, list)
            ),
            []
        )

    if not isinstance(data, list):

        print(
            "\nEl formato de respuesta de células "
            "no es una lista."
        )

        print(data)

        return []

    resultado = []

    for item in data:

        if not isinstance(item, dict):
            continue

        # Convertimos las claves a minúsculas
        # para soportar Id/id y Nombre/nombre.
        low = {
            str(key).lower(): value
            for key, value in item.items()
        }

        if "id" in low and "nombre" in low:

            resultado.append(
                (
                    low["id"],
                    low["nombre"]
                )
            )

    return resultado


# ============================================================
# CREAR CONSULTOR
# ============================================================

def crear_consultor(session, celula_id):

    payload = dict(PERSONA_PRUEBA)

    # CrearConsultorDto espera:
    #
    # List<CelulaAsignacionDto>
    #
    # donde CelulaAsignacionDto tiene:
    # CelulaId
    # PorcentajeParticipacion

    payload["Celulas"] = [
        {
            "CelulaId": celula_id,
            "PorcentajeParticipacion": None
        }
    ]

    print("\nCreando consultor...")
    print(f"Célula asignada: {celula_id}")

    try:

        response = session.post(
            API_URL + CONSULTORES_PATH,
            json=payload,
            timeout=60
        )

    except requests.exceptions.RequestException as e:

        sys.exit(
            "\nError conectando con el endpoint "
            "de consultores:\n"
            f"{e}"
        )

    ok = response.status_code < 300

    print(
        f"\nResultado: "
        f"{'OK' if ok else 'ERROR'} "
        f"(HTTP {response.status_code})"
    )

    print(
        response.text[:1000]
    )

    if ok:

        print(
            "\n============================================"
        )

        print(
            "CONSULTOR CREADO CORRECTAMENTE"
        )

        print(
            "============================================"
        )

        print(
            "Email: prueba.carga@example.com"
        )

        print(
            "\nEl email es único."
        )

        print(
            "Si vuelves a ejecutar la prueba, "
            "probablemente tendrás que cambiarlo "
            "o eliminar/deshabilitar el registro anterior."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "============================================"
    )

    print(
        " PRUEBA DE CREACIÓN DE CONSULTOR"
    )

    print(
        "============================================"
    )

    print(
        f"\nAPI: {API_URL}"
    )

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    session = login()

    # --------------------------------------------------------
    # OBTENER CÉLULAS
    # --------------------------------------------------------

    celulas = listar_celulas(session)

    if celulas:

        print(
            "\nCélulas disponibles:"
        )

        for celula_id, nombre in celulas:

            print(
                f"  ID: {celula_id} | Nombre: {nombre}"
            )

    else:

        print(
            "\nNo pude listar células."
        )

    # --------------------------------------------------------
    # SELECCIONAR CÉLULA
    # --------------------------------------------------------

    if CELULA_ID_PRUEBA is not None:

        celula_id = CELULA_ID_PRUEBA

        print(
            f"\nUsando célula configurada manualmente: "
            f"{celula_id}"
        )

    elif celulas:

        # Utiliza la primera célula encontrada

        celula_id = celulas[0][0]

        print(
            f"\nUsando automáticamente la primera célula:"
            f" {celula_id}"
        )

    else:

        sys.exit(
            "\nNo hay una célula disponible para asignar.\n"
            "Configura CELULA_ID_PRUEBA con el ID "
            "de una célula existente."
        )

    # --------------------------------------------------------
    # CREAR CONSULTOR
    # --------------------------------------------------------

    crear_consultor(
        session,
        celula_id
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
