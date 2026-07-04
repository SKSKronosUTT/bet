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
# slot 0 -> se queda con los partidos 0,1 (España-Portugal, Alemania-Inglaterra)
# slot 1 -> se queda con los partidos 2,3 (Holanda-Eslovaquia, Brasil-Chile)
# Si alguien entra con otro nombre, se le asigna el primer slot libre.
# --------------------------------------------------------------------------
JUGADORES_ESPERADOS = ["Arzola", "Yivy"]

# --------------------------------------------------------------------------
# Octavos de final del Mundial 2010, más la Final real (Holanda vs España).
# El último partido de la lista de cada jugador es el que está forzado a
# perderse pase lo que pase, para que la quiniela completa truene justo
# antes de la Final.
# --------------------------------------------------------------------------
PARTIDOS = [
    {"id": 0, "equipo1": "España",   "bandera1": "🇪🇸", "equipo2": "Portugal",   "bandera2": "🇵🇹"},
    {"id": 1, "equipo1": "Alemania", "bandera1": "🇩🇪", "equipo2": "Inglaterra", "bandera2": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
    {"id": 2, "equipo1": "Holanda",  "bandera1": "🇳🇱", "equipo2": "Eslovaquia", "bandera2": "🇸🇰"},
    {"id": 3, "equipo1": "Brasil",   "bandera1": "🇧🇷", "equipo2": "Chile",      "bandera2": "🇨🇱"},
]

# La Final real del Mundial 2010: Holanda 0 - España 1 (gol de Iniesta).
PARTIDO_BONO = {
    "id": len(PARTIDOS),
    "equipo1": "Holanda", "bandera1": "🇳🇱",
    "equipo2": "España",  "bandera2": "🇪🇸",
}

# Marcador fijo (histórico) del partido bono: Holanda 0 - España 1
FINAL_MARCADOR = (0, 1)

NUM_PARTIDOS_PRINCIPALES = len(PARTIDOS)
ID_PARTIDO_BONO = PARTIDO_BONO["id"]

# Partidos que le tocan a cada slot (indices dentro de PARTIDOS)
PARTIDOS_POR_SLOT = {
    0: [0, 1],
    1: [2, 3],
}

# Posibles goleadores por selección (para las animaciones de gol).
JUGADORES_POR_EQUIPO = {
    "España": ["David Villa", "Fernando Torres"],
    "Portugal": ["Cristiano Ronaldo"],
    "Alemania": ["Thomas Müller", "Mesut Özil"],
    "Inglaterra": ["Wayne Rooney", "Frank Lampard"],
    "Holanda": ["Robin van Persie", "Arjen Robben"],
    "Eslovaquia": ["Filip Hološko"],
    "Brasil": ["Neymar", "Ronaldinho"],
    "Chile": ["Alexis Sánchez"],
}

# Tipos de apuesta disponibles por partido y su "cuota" decimal.
# (todas dan momio americano positivo, entre +100 y +300 aprox; la cuota
# solo es para mostrar la "ganancia potencial" en pantalla, el resultado
# real de la quiniela ya está decidido de antemano)
TIPOS_APUESTA = {
    "equipo1": {"cuota": 2.4},
    "empate":  {"cuota": 3.0},
    "equipo2": {"cuota": 2.6},
    "over":    {"cuota": 2.1},
    "under":   {"cuota": 2.15},
}

# Duracion de la animacion de un partido (milisegundos por "minuto" simulado)
MS_POR_MINUTO = 160  # 90 minutos * 160ms = 14.4s por partido aprox


def partidos_de_slot(slot):
    """IDs de los partidos que le tocan a un slot, en orden."""
    return PARTIDOS_POR_SLOT[slot]


def es_partido_truco(slot, match_id):
    """True si este partido es el que esta forzado a perderse para ese slot
    (siempre el último de la lista de ese jugador)."""
    partidos = partidos_de_slot(slot)
    return match_id == partidos[-1]


def slot_del_partido(match_id):
    """A que slot le pertenece un match_id normal (None si es el bono)."""
    for slot, ids in PARTIDOS_POR_SLOT.items():
        if match_id in ids:
            return slot
    return None
