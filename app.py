# -*- coding: utf-8 -*-
"""
Quiniela de cumpleaños - app principal de Flask.

Dos pantallas:
  /anfitrion  -> se proyecta en la tele, la controla el anfitrión (tú).
  /jugar      -> se abre en el celular de cada invitado (via QR).

Todo el estado vive en SQLite (db.py) y se sincroniza por polling
sencillo (fetch cada 1-2 segundos), nada de websockets ni hilos en
segundo plano, para que sea trivial de correr en PythonAnywhere.
"""

from flask import Flask, jsonify, render_template, request, session, redirect, url_for

import config
import db
import game_logic

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

db.init_db(app)

BONO_ID = config.ID_PARTIDO_BONO
NUM_PRINCIPALES = config.NUM_PARTIDOS_PRINCIPALES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def current_player():
    player_id = session.get("player_id")
    if not player_id:
        return None
    conn = db.get_db()
    return db.get_player(conn, player_id)


def player_public(p, conn):
    """Representación de un jugador + sus apuestas, lista para mandar a JSON."""
    slot_matches = config.partidos_de_slot(p["slot"])
    bets = {b["match_id"]: b for b in db.get_bets_for_player(conn, p["id"])}
    partidos = []
    for mid in slot_matches:
        m = db.get_match(conn, mid)
        bet = bets.get(mid)
        terminado = m["status"] == "finished"
        partidos.append({
            "id": mid,
            "equipo1": m["equipo1"], "bandera1": m["bandera1"],
            "equipo2": m["equipo2"], "bandera2": m["bandera2"],
            "status": m["status"],
            "es_truco": config.es_partido_truco(p["slot"], mid),
            "apuesta": bet["bet_type"] if bet else None,
            "apuesta_status": bet["status"] if bet else None,
            "apuesta_label": game_logic.nombre_tipo_apuesta(bet["bet_type"], m["equipo1"], m["equipo2"]) if bet else None,
            "marcador1": m["marcador1"] if terminado else None,
            "marcador2": m["marcador2"] if terminado else None,
        })

    bono = db.get_match(conn, BONO_ID)
    bono_bet = db.get_bet(conn, p["id"], BONO_ID)
    bono_info = {
        "id": BONO_ID,
        "equipo1": bono["equipo1"], "bandera1": bono["bandera1"],
        "equipo2": bono["equipo2"], "bandera2": bono["bandera2"],
        "status": bono["status"],
        "apuesta": bono_bet["bet_type"] if bono_bet else None,
        "apuesta_status": bono_bet["status"] if bono_bet else None,
    }

    tipos_elegidos = [b["bet_type"] for b in bets.values()]
    multiplicador = game_logic.calcular_multiplicador(tipos_elegidos) if len(tipos_elegidos) == len(slot_matches) else None

    return {
        "id": p["id"],
        "username": p["username"],
        "slot": p["slot"],
        "balance": p["balance"],
        "parlay_submitted": bool(p["parlay_submitted"]),
        "bonus_added": bool(p["bonus_added"]),
        "bonus_bet_submitted": bool(p["bonus_bet_submitted"]),
        "partidos": partidos,
        "bono": bono_info,
        "multiplicador_potencial": multiplicador,
    }


def match_public(m, revelar_marcador):
    goles = None
    marcador1 = marcador2 = None
    if revelar_marcador and m["status"] in ("live", "finished"):
        marcador1, marcador2 = m["marcador1"], m["marcador2"]
        if m["goles_json"]:
            import json
            goles = json.loads(m["goles_json"])
    return {
        "id": m["id"],
        "equipo1": m["equipo1"], "bandera1": m["bandera1"],
        "equipo2": m["equipo2"], "bandera2": m["bandera2"],
        "es_bono": bool(m["es_bono"]),
        "status": m["status"],
        "marcador1": marcador1,
        "marcador2": marcador2,
        "goles": goles,
        "duracion_ms": 90 * config.MS_POR_MINUTO,
    }


def asignar_slot(jugadores_actuales, username):
    esperados = [n.lower() for n in config.JUGADORES_ESPERADOS]
    ocupados = {p["slot"] for p in jugadores_actuales}
    lower = username.lower()
    if lower in esperados:
        deseado = esperados.index(lower)
        if deseado not in ocupados:
            return deseado
    for slot in sorted(config.PARTIDOS_POR_SLOT.keys()):
        if slot not in ocupados:
            return slot
    return None


# ---------------------------------------------------------------------------
# Páginas
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    return redirect(url_for("anfitrion"))


@app.get("/anfitrion")
def anfitrion():
    join_url = url_for("jugador", _external=True)
    return render_template(
        "host.html",
        join_url=join_url,
        nombres_esperados=config.JUGADORES_ESPERADOS,
    )


@app.get("/jugar")
def jugador():
    return render_template(
        "player.html",
        nombres_sugeridos=config.JUGADORES_ESPERADOS,
        momios=game_logic.momios_americanos(),
    )


# ---------------------------------------------------------------------------
# API - estado general (lo usan tanto la tele como los celulares)
# ---------------------------------------------------------------------------

@app.get("/api/estado")
def api_estado():
    conn = db.get_db()
    estado = db.get_state(conn)
    jugadores = [player_public(p, conn) for p in db.get_players(conn)]

    fase = estado["phase"]
    match_index = estado["match_index"]

    partido_actual = None
    if fase == "playing" and match_index < NUM_PRINCIPALES:
        m = db.get_match(conn, match_index)
        partido_actual = match_public(m, revelar_marcador=True)
    elif fase in ("bono_playing", "bono_intro", "bono_apuestas"):
        m = db.get_match(conn, BONO_ID)
        partido_actual = match_public(m, revelar_marcador=(fase == "bono_playing"))

    todos_partidos = [match_public(m, revelar_marcador=(m["status"] == "finished")) for m in db.get_matches(conn)]

    return jsonify({
        "fase": fase,
        "match_index": match_index,
        "jugadores": jugadores,
        "partido_actual": partido_actual,
        "partidos": todos_partidos,
    })


@app.get("/api/mi-estado")
def api_mi_estado():
    p = current_player()
    if not p:
        return jsonify({"registrado": False})
    conn = db.get_db()
    estado = db.get_state(conn)
    data = player_public(p, conn)
    data["registrado"] = True
    data["fase"] = estado["phase"]
    return jsonify(data)


# ---------------------------------------------------------------------------
# API - registro y apuestas de jugador
# ---------------------------------------------------------------------------

@app.post("/api/registro")
def api_registro():
    conn = db.get_db()

    existing_id = session.get("player_id")
    if existing_id:
        p = db.get_player(conn, existing_id)
        if p:
            return jsonify(player_public(p, conn))

    data = request.get_json(force=True, silent=True) or {}
    username = (data.get("username") or "").strip()
    if not username or len(username) > 24:
        return jsonify(error="Escribe un nombre válido (máximo 24 caracteres)."), 400

    same_name = db.get_player_by_username(conn, username)
    if same_name:
        session["player_id"] = same_name["id"]
        return jsonify(player_public(same_name, conn))

    estado = db.get_state(conn)
    if estado["phase"] != "lobby":
        return jsonify(error="La partida ya comenzó, no se pueden agregar más jugadores."), 400

    jugadores = db.get_players(conn)
    if len(jugadores) >= len(config.JUGADORES_ESPERADOS):
        return jsonify(error="Ya no hay lugares disponibles en esta partida."), 400

    slot = asignar_slot(jugadores, username)
    if slot is None:
        return jsonify(error="Ya no hay lugares disponibles en esta partida."), 400

    player = db.create_player(conn, username, slot)
    session["player_id"] = player["id"]
    return jsonify(player_public(player, conn))


@app.post("/api/apostar")
def api_apostar():
    p = current_player()
    if not p:
        return jsonify(error="No estás registrado."), 403

    conn = db.get_db()
    estado = db.get_state(conn)
    if estado["phase"] != "betting":
        return jsonify(error="Todavía no es momento de apostar."), 400
    if p["parlay_submitted"]:
        return jsonify(error="Ya registraste tu parley."), 400

    data = request.get_json(force=True, silent=True) or {}
    apuestas = data.get("apuestas") or {}

    partidos_slot = set(config.partidos_de_slot(p["slot"]))
    try:
        ids_recibidos = {int(k) for k in apuestas.keys()}
    except (TypeError, ValueError):
        return jsonify(error="Apuestas inválidas."), 400

    if ids_recibidos != partidos_slot:
        return jsonify(error=f"Debes apostar en tus {len(partidos_slot)} partidos, ni más ni menos."), 400

    tipos_validos = set(config.TIPOS_APUESTA.keys())
    for tipo in apuestas.values():
        if tipo not in tipos_validos:
            return jsonify(error="Hay un tipo de apuesta inválido."), 400

    for mid_str, tipo in apuestas.items():
        mid = int(mid_str)
        m = db.get_match(conn, mid)
        debe_ganar = not config.es_partido_truco(p["slot"], mid)
        m1, m2 = game_logic.generar_marcador(tipo, debe_ganar)
        goles = game_logic.generar_eventos_goles(m1, m2, m["equipo1"], m["equipo2"])
        db.set_match_result(conn, mid, m1, m2, goles)
        db.create_bet(conn, p["id"], mid, tipo)

    db.mark_parlay_submitted(conn, p["id"])
    return jsonify(ok=True)


@app.post("/api/apostar-bono")
def api_apostar_bono():
    p = current_player()
    if not p:
        return jsonify(error="No estás registrado."), 403

    conn = db.get_db()
    estado = db.get_state(conn)
    if estado["phase"] != "bono_apuestas":
        return jsonify(error="Todavía no es momento de la apuesta final."), 400
    if not p["bonus_added"]:
        return jsonify(error="Aún no tienes saldo para la apuesta final."), 400
    if p["bonus_bet_submitted"]:
        return jsonify(error="Ya hiciste tu apuesta final."), 400

    data = request.get_json(force=True, silent=True) or {}
    tipo = data.get("tipo")
    if tipo not in ("equipo1", "empate", "equipo2"):
        return jsonify(error="Elige un resultado válido."), 400

    db.create_bet(conn, p["id"], BONO_ID, tipo)
    db.mark_bonus_bet_submitted(conn, p["id"])
    return jsonify(ok=True)


# ---------------------------------------------------------------------------
# API - controles del anfitrión
# ---------------------------------------------------------------------------

def _requiere_fase(conn, fase_esperada):
    estado = db.get_state(conn)
    if estado["phase"] != fase_esperada:
        return False
    return True


@app.post("/api/host/iniciar-apuestas")
def host_iniciar_apuestas():
    conn = db.get_db()
    if not _requiere_fase(conn, "lobby"):
        return jsonify(error="Fase incorrecta."), 400
    if len(db.get_players(conn)) < len(config.JUGADORES_ESPERADOS):
        return jsonify(error="Todavía faltan jugadores por unirse."), 400
    db.set_phase(conn, "betting")
    return jsonify(ok=True)


@app.post("/api/host/comenzar-partidos")
def host_comenzar_partidos():
    conn = db.get_db()
    if not _requiere_fase(conn, "betting"):
        return jsonify(error="Fase incorrecta."), 400
    jugadores = db.get_players(conn)
    if not all(p["parlay_submitted"] for p in jugadores):
        return jsonify(error="Todavía falta que alguien registre su parley."), 400
    db.set_match_index(conn, 0)
    db.set_phase(conn, "playing")
    return jsonify(ok=True)


@app.post("/api/host/reproducir-partido")
def host_reproducir_partido():
    conn = db.get_db()
    estado = db.get_state(conn)
    if estado["phase"] != "playing":
        return jsonify(error="Fase incorrecta."), 400
    match_id = estado["match_index"]
    db.set_match_status(conn, match_id, "live")
    return jsonify(ok=True)


@app.post("/api/host/finalizar-partido")
def host_finalizar_partido():
    conn = db.get_db()
    estado = db.get_state(conn)
    if estado["phase"] != "playing":
        return jsonify(error="Fase incorrecta."), 400
    match_id = estado["match_index"]
    m = db.get_match(conn, match_id)
    if m["status"] != "live":
        return jsonify(error="Este partido no está en curso."), 400

    slot = config.slot_del_partido(match_id)
    jugador_dueno = db.get_player_by_slot(conn, slot)
    if jugador_dueno:
        bet = db.get_bet(conn, jugador_dueno["id"], match_id)
        if bet:
            gano = game_logic.resolver_apuesta(bet["bet_type"], m["marcador1"], m["marcador2"])
            db.set_bet_status(conn, bet["id"], "ganada" if gano else "perdida")

    db.set_match_status(conn, match_id, "finished")

    siguiente = match_id + 1
    if siguiente >= NUM_PRINCIPALES:
        db.set_phase(conn, "bono_intro")
    else:
        db.set_match_index(conn, siguiente)
    return jsonify(ok=True)


@app.post("/api/host/revelar-bono")
def host_revelar_bono():
    conn = db.get_db()
    if not _requiere_fase(conn, "bono_intro"):
        return jsonify(error="Fase incorrecta."), 400
    for p in db.get_players(conn):
        db.set_player_balance(conn, p["id"], config.SALDO_BONO)
        db.mark_bonus_added(conn, p["id"])
    db.set_phase(conn, "bono_apuestas")
    return jsonify(ok=True)


@app.post("/api/host/comenzar-bono")
def host_comenzar_bono():
    conn = db.get_db()
    if not _requiere_fase(conn, "bono_apuestas"):
        return jsonify(error="Fase incorrecta."), 400
    jugadores = db.get_players(conn)
    if not all(p["bonus_bet_submitted"] for p in jugadores):
        return jsonify(error="Todavía falta la apuesta final de alguien."), 400
    m1, m2 = config.FINAL_MARCADOR
    bono_match = db.get_match(conn, BONO_ID)
    goles = game_logic.generar_eventos_goles(m1, m2, bono_match["equipo1"], bono_match["equipo2"])
    db.set_match_result(conn, BONO_ID, m1, m2, goles)
    db.set_phase(conn, "bono_playing")
    return jsonify(ok=True)


@app.post("/api/host/reproducir-bono")
def host_reproducir_bono():
    conn = db.get_db()
    if not _requiere_fase(conn, "bono_playing"):
        return jsonify(error="Fase incorrecta."), 400
    db.set_match_status(conn, BONO_ID, "live")
    return jsonify(ok=True)


@app.post("/api/host/finalizar-bono")
def host_finalizar_bono():
    conn = db.get_db()
    if not _requiere_fase(conn, "bono_playing"):
        return jsonify(error="Fase incorrecta."), 400
    for p in db.get_players(conn):
        bet = db.get_bet(conn, p["id"], BONO_ID)
        if bet:
            db.set_bet_status(conn, bet["id"], "ganada")
            pago = game_logic.calcular_pago_bono(p["balance"])
            db.set_player_balance(conn, p["id"], pago)
    db.set_match_status(conn, BONO_ID, "finished")
    db.set_phase(conn, "end")
    return jsonify(ok=True)


@app.post("/api/host/reiniciar")
def host_reiniciar():
    conn = db.get_db()
    db.reset_game(conn)
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
