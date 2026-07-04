# -*- coding: utf-8 -*-
"""
Aqui vive la "trampa" del juego: dado el pronostico que eligio un jugador,
generamos un marcador de partido que hace que ese pronostico gane o pierda,
segun lo que necesitemos para la historia de la noche.

Nada de esto es una simulacion real de futbol, es un generador de marcadores
que hace match con el resultado narrativo que queremos: los pronosticos de
cada quien se cumplen menos el ultimo, que siempre truena, y la Final
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


def elegir_goleador(nombre_equipo):
    """Escoge (al azar, con reemplazo) quién anotó un gol de ese equipo."""
    plantilla = config.JUGADORES_POR_EQUIPO.get(nombre_equipo)
    if not plantilla:
        return nombre_equipo
    return random.choice(plantilla)


def generar_eventos_goles(m1, m2, equipo1, equipo2):
    """Lista de goles [{minuto, equipo, jugador}] ordenada, para animar el partido."""
    total = m1 + m2
    if total == 0:
        return []
    minutos = sorted(random.sample(range(3, 89), total))
    equipos = [1] * m1 + [2] * m2
    random.shuffle(equipos)
    eventos = []
    for minuto, equipo in zip(minutos, equipos):
        nombre_equipo = equipo1 if equipo == 1 else equipo2
        eventos.append({
            "minuto": minuto,
            "equipo": equipo,
            "jugador": elegir_goleador(nombre_equipo),
        })
    return eventos


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


def decimal_a_americano(cuota):
    """Convierte una cuota decimal (ej. 2.4) a momio americano (ej. '+140')."""
    if cuota >= 2.0:
        valor = round((cuota - 1) * 100)
        return f"+{valor}"
    valor = round(-100 / (cuota - 1))
    return str(valor)


def momios_americanos():
    """Diccionario {tipo: '+140'} listo para mandar al frontend."""
    return {tipo: decimal_a_americano(datos["cuota"]) for tipo, datos in config.TIPOS_APUESTA.items()}
