# -*- coding: utf-8 -*-
"""
Capa de acceso a datos. Sqlite puro, sin ORM, para que sea facil de leer
y de instalar en PythonAnywhere (no requiere nada extra a Flask).
"""

import json
import sqlite3

from flask import g

import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS game_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    phase TEXT NOT NULL DEFAULT 'lobby',
    match_index INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    slot INTEGER NOT NULL,
    balance REAL NOT NULL DEFAULT 0,
    parlay_submitted INTEGER NOT NULL DEFAULT 0,
    bonus_added INTEGER NOT NULL DEFAULT 0,
    bonus_bet_submitted INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY,
    equipo1 TEXT NOT NULL,
    bandera1 TEXT NOT NULL,
    equipo2 TEXT NOT NULL,
    bandera2 TEXT NOT NULL,
    es_bono INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'pending',
    marcador1 INTEGER,
    marcador2 INTEGER,
    goles_json TEXT
);

CREATE TABLE IF NOT EXISTS bets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    bet_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'abierta',
    UNIQUE(player_id, match_id)
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(config.DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        db = get_db()
        db.executescript(SCHEMA)
        db.commit()
        _seed_if_empty(db)


def _seed_if_empty(db):
    row = db.execute("SELECT COUNT(*) AS c FROM game_state").fetchone()
    if row["c"] == 0:
        db.execute("INSERT INTO game_state (id, phase, match_index) VALUES (1, 'lobby', 0)")

    row = db.execute("SELECT COUNT(*) AS c FROM matches").fetchone()
    if row["c"] == 0:
        for p in config.PARTIDOS:
            db.execute(
                "INSERT INTO matches (id, equipo1, bandera1, equipo2, bandera2, es_bono) "
                "VALUES (?, ?, ?, ?, ?, 0)",
                (p["id"], p["equipo1"], p["bandera1"], p["equipo2"], p["bandera2"]),
            )
        b = config.PARTIDO_BONO
        db.execute(
            "INSERT INTO matches (id, equipo1, bandera1, equipo2, bandera2, es_bono) "
            "VALUES (?, ?, ?, ?, ?, 1)",
            (b["id"], b["equipo1"], b["bandera1"], b["equipo2"], b["bandera2"]),
        )
    db.commit()


def reset_game(db):
    """Regresa todo a cero por si se quiere volver a jugar."""
    db.execute("DELETE FROM bets")
    db.execute("DELETE FROM players")
    db.execute(
        "UPDATE matches SET status = 'pending', marcador1 = NULL, marcador2 = NULL, goles_json = NULL"
    )
    db.execute("UPDATE game_state SET phase = 'lobby', match_index = 0 WHERE id = 1")
    db.commit()


# ---------------------------------------------------------------------------
# game_state
# ---------------------------------------------------------------------------

def get_state(db):
    return db.execute("SELECT * FROM game_state WHERE id = 1").fetchone()


def set_phase(db, phase):
    db.execute("UPDATE game_state SET phase = ? WHERE id = 1", (phase,))
    db.commit()


def set_match_index(db, index):
    db.execute("UPDATE game_state SET match_index = ? WHERE id = 1", (index,))
    db.commit()


# ---------------------------------------------------------------------------
# players
# ---------------------------------------------------------------------------

def get_players(db):
    return db.execute("SELECT * FROM players ORDER BY slot ASC").fetchall()


def get_player(db, player_id):
    return db.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()


def get_player_by_username(db, username):
    return db.execute(
        "SELECT * FROM players WHERE lower(username) = lower(?)", (username,)
    ).fetchone()


def get_player_by_slot(db, slot):
    return db.execute("SELECT * FROM players WHERE slot = ?", (slot,)).fetchone()


def create_player(db, username, slot):
    cur = db.execute(
        "INSERT INTO players (username, slot, balance) VALUES (?, ?, ?)",
        (username, slot, config.SALDO_INICIAL),
    )
    db.commit()
    return get_player(db, cur.lastrowid)


def set_player_balance(db, player_id, balance):
    db.execute("UPDATE players SET balance = ? WHERE id = ?", (balance, player_id))
    db.commit()


def mark_parlay_submitted(db, player_id):
    db.execute("UPDATE players SET parlay_submitted = 1 WHERE id = ?", (player_id,))
    db.commit()


def mark_bonus_added(db, player_id):
    db.execute("UPDATE players SET bonus_added = 1 WHERE id = ?", (player_id,))
    db.commit()


def mark_bonus_bet_submitted(db, player_id):
    db.execute("UPDATE players SET bonus_bet_submitted = 1 WHERE id = ?", (player_id,))
    db.commit()


# ---------------------------------------------------------------------------
# matches
# ---------------------------------------------------------------------------

def get_matches(db):
    return db.execute("SELECT * FROM matches ORDER BY id ASC").fetchall()


def get_match(db, match_id):
    return db.execute("SELECT * FROM matches WHERE id = ?", (match_id,)).fetchone()


def set_match_result(db, match_id, marcador1, marcador2, goles):
    db.execute(
        "UPDATE matches SET marcador1 = ?, marcador2 = ?, goles_json = ? WHERE id = ?",
        (marcador1, marcador2, json.dumps(goles), match_id),
    )
    db.commit()


def set_match_status(db, match_id, status):
    db.execute("UPDATE matches SET status = ? WHERE id = ?", (status, match_id))
    db.commit()


# ---------------------------------------------------------------------------
# bets
# ---------------------------------------------------------------------------

def create_bet(db, player_id, match_id, bet_type):
    db.execute(
        "INSERT OR REPLACE INTO bets (player_id, match_id, bet_type, status) "
        "VALUES (?, ?, ?, 'abierta')",
        (player_id, match_id, bet_type),
    )
    db.commit()


def get_bets_for_player(db, player_id):
    return db.execute(
        "SELECT * FROM bets WHERE player_id = ? ORDER BY match_id ASC", (player_id,)
    ).fetchall()


def get_bet(db, player_id, match_id):
    return db.execute(
        "SELECT * FROM bets WHERE player_id = ? AND match_id = ?", (player_id, match_id)
    ).fetchone()


def set_bet_status(db, bet_id, status):
    db.execute("UPDATE bets SET status = ? WHERE id = ?", (status, bet_id))
    db.commit()
