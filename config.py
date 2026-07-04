# -*- coding: utf-8 -*-
"""
Configuracion central del juego.
Aqui se define quienes juegan, que partidos hay y como se reparten.
Si algun dia quieres reusar esto para otra fiesta, este es el unico
archivo que necesitas tocar.
"""

import os

# Llave secreta de Flask (para las cookies de sesion de cada jugador).
# En PythonAnywhere puedes sobreescribirla con una variable de entorno.
SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esto-antes-de-subirlo-a-produccion")

# Saldo inicial con el que arranca cada jugador
SALDO_INICIAL = 10.0

# Cuanto se le agrega para la "ultima oportunidad"
SALDO_BONO = 1.0

# Momio americano de la ultima apuesta (para que 1 peso se convierta en 100)
MOMIO_BONO = 9900

# Nombre de archivo de la base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiniela.db")

# --------------------------------------------------------------------------
# Jugadores esperados. El nombre se compara sin mayusculas/acentos raros.
# slot 0 -> se queda con los partidos 0,1,2
# slot 1 -> se queda con los partidos 3,4,5
# Si alguien entra con otro nombre, se le asigna el primer slot libre.
# --------------------------------------------------------------------------
JUGADORES_ESPERADOS = ["Arzola", "Yivy"]

# --------------------------------------------------------------------------
# Los 6 partidos "normales" + 1 partido bonus (index 6).
# El ultimo partido de cada tanda (index 2 y 5) es el que esta forzado a
# perderse pase lo que pase, para que la quiniela completa truene justo
# antes del final.
# --------------------------------------------------------------------------
PARTIDOS = [
    {"id": 0, "equipo1": "Francia",        "bandera1": "🇫🇷", "equipo2": "Alemania",  "bandera2": "🇩🇪"},
    {"id": 1, "equipo1": "Estados Unidos", "bandera1": "🇺🇸", "equipo2": "Bélgica",   "bandera2": "🇧🇪"},
    {"id": 2, "equipo1": "España",         "bandera1": "🇪🇸", "equipo2": "Portugal",  "bandera2": "🇵🇹"},
    {"id": 3, "equipo1": "México",         "bandera1": "🇲🇽", "equipo2": "Inglaterra","bandera2": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
    {"id": 4, "equipo1": "Suiza",          "bandera1": "🇨🇭", "equipo2": "Colombia",  "bandera2": "🇨🇴"},
    {"id": 5, "equipo1": "Argentina",      "bandera1": "🇦🇷", "equipo2": "Egipto",    "bandera2": "🇪🇬"},
]

PARTIDO_BONO = {"id": 6, "equipo1": "Francia", "bandera1": "🇫🇷", "equipo2": "Argentina", "bandera2": "🇦🇷"}

# Partidos que le tocan a cada slot (indices dentro de PARTIDOS)
PARTIDOS_POR_SLOT = {
    0: [0, 1, 2],
    1: [3, 4, 5],
}

# El ultimo partido de la lista de cada slot es el que se fuerza a perder
INDICE_PARTIDO_TRUCO = 2  # posicion dentro de la lista de 3 (0,1,2) -> el tercero

# Tipos de apuesta disponibles por partido y su "cuota" decimal
# (la cuota solo es para que se vea la ganancia potencial en pantalla,
# el resultado real de la quiniela ya esta decidido de antemano)
TIPOS_APUESTA = {
    "equipo1": {"cuota": 2.4},
    "empate":  {"cuota": 3.1},
    "equipo2": {"cuota": 2.7},
    "over":    {"cuota": 1.85},
    "under":   {"cuota": 1.95},
}

# Duracion de la animacion de un partido (milisegundos por "minuto" simulado)
MS_POR_MINUTO = 160  # 90 minutos * 160ms = 14.4s por partido aprox


def partidos_de_slot(slot):
    """IDs de los 3 partidos que le tocan a un slot, en orden."""
    return PARTIDOS_POR_SLOT[slot]


def es_partido_truco(slot, match_id):
    """True si este partido es el que esta forzado a perderse para ese slot."""
    partidos = partidos_de_slot(slot)
    return match_id == partidos[INDICE_PARTIDO_TRUCO]


def slot_del_partido(match_id):
    """A que slot le pertenece un match_id normal (None si es el bono)."""
    for slot, ids in PARTIDOS_POR_SLOT.items():
        if match_id in ids:
            return slot
    return None

