# -*- coding: utf-8 -*-
"""
Aqui vive la "trampa" del juego: dado el pronostico que eligio un jugador,
generamos un marcador de partido que hace que ese pronostico gane o pierda,
segun lo que necesitemos para la historia de la noche.

Nada de esto es una simulacion real de futbol, es un generador de marcadores
que hace match con el resultado narrativo que queremos: los primeros dos
pronosticos de cada quien se cumplen, el tercero truena, y el partido bono
siempre paga.
"""

import random

import config

# Marcadores curados por tipo de apuesta y por si tiene que ganar o perder.
# Se eligieron marcadores "creibles" de futbol, nada de 7-6.
_CANDIDATOS = {
    ("equipo1", True):  [(1, 0), (2, 0), (2, 1), (3, 1), (3, 2)],
    ("equipo1", False): [(0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (0, 2)],
    ("equipo2", True):  [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)],
    ("equipo2", False): [(0, 0), (1, 1), (2, 2), (1, 0), (2, 0), (2, 1)],
    ("empate", True):   [(0, 0), (1, 1), (2, 2)],
    ("empate", False):  [(1, 0), (0, 1), (2, 0), (0, 2), (2, 1), (1, 2), (3, 1)],
    ("over", True):     [(2, 1), (3, 1), (2, 2), (3, 0), (1, 2), (3, 2)],
    ("over", False):    [(0, 0), (1, 0), (0, 1), (1, 1)],
    ("under", True):    [(0, 0), (1, 0), (0, 1), (1, 1)],
    ("under", False):   [(2, 1), (1, 2), (3, 0), (0, 3), (2, 2), (3, 1)],
}


def resolver_apuesta(tipo, m1, m2):
    """True si el marcador (m1, m2) hace ganar una apuesta de este tipo."""
    if tipo == "equipo1":
        return m1 > m2
    if tipo == "equipo2":
        return m2 > m1
    if tipo == "empate":
        return m1 == m2
    if tipo == "over":
        return (m1 + m2) >= 3
    if tipo == "under":
        return (m1 + m2) <= 2
    raise ValueError(f"Tipo de apuesta desconocido: {tipo}")


def generar_marcador(tipo, debe_ganar):
    """Regresa un marcador (m1, m2) que resuelve la apuesta como se pida."""
    candidatos = _CANDIDATOS[(tipo, debe_ganar)]
    return random.choice(candidatos)


def generar_marcador_libre():
    """Marcador sin restricciones, solo para el 'sabor' del partido bono."""
    opciones = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (2, 0), (0, 2)]
    return random.choice(opciones)


def generar_eventos_goles(m1, m2):
    """Lista de goles [{minuto, equipo}] ordenada, para animar el partido."""
    total = m1 + m2
    if total == 0:
        return []
    minutos = sorted(random.sample(range(3, 89), total))
    equipos = [1] * m1 + [2] * m2
    random.shuffle(equipos)
    return [{"minuto": minuto, "equipo": equipo} for minuto, equipo in zip(minutos, equipos)]


def calcular_multiplicador(tipos_apuesta):
    """Multiplicador combinado de una parley (solo para mostrar 'ganancia potencial')."""
    total = 1.0
    for t in tipos_apuesta:
        total *= config.TIPOS_APUESTA[t]["cuota"]
    return round(total, 2)


def calcular_pago_bono(apuesta):
    """Momio americano +9900: profit = apuesta * (momio / 100)."""
    ganancia = apuesta * (config.MOMIO_BONO / 100.0)
    return round(apuesta + ganancia, 2)


def nombre_tipo_apuesta(tipo, equipo1, equipo2):
    etiquetas = {
        "equipo1": f"Gana {equipo1}",
        "equipo2": f"Gana {equipo2}",
        "empate": "Empate",
        "over": "Más de 2.5 goles",
        "under": "Menos de 2.5 goles",
    }
    return etiquetas.get(tipo, tipo)
