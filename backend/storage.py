import uuid, os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

DB_URL = os.getenv("DB_URL", "sqlite:///textmood.db")
engine: Engine = create_engine(DB_URL, future=True)

def init_db():
    with engine.begin() as conn:
        conn.exec_driver_sql("""
        CREATE TABLE IF NOT EXISTS sessions(
            session_id TEXT PRIMARY KEY,
            created_at TEXT,
            last_seen TEXT,
            user_agent TEXT
        );
        """)
        conn.exec_driver_sql("""
        CREATE TABLE IF NOT EXISTS interactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            text TEXT,
            emotion TEXT,
            created_at TEXT
        );
        """)

def new_session(user_agent: str|None) -> str:
    sid = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    with engine.begin() as conn:
        conn.exec_driver_sql(
            "INSERT INTO sessions(session_id, created_at, last_seen, user_agent) VALUES(?,?,?,?)",
            (sid, now, now, user_agent or "")
        )
    return sid

def touch_session(session_id: str):
    with engine.begin() as conn:
        conn.exec_driver_sql(
            "UPDATE sessions SET last_seen=? WHERE session_id=?",
            (datetime.utcnow().isoformat(), session_id)
        )

def add_interaction(session_id: str, textval: str, emotion: str):
    with engine.begin() as conn:
        conn.exec_driver_sql(
            "INSERT INTO interactions(session_id, text, emotion, created_at) VALUES(?,?,?,?)",
            (session_id, textval, emotion, datetime.utcnow().isoformat())
        )

def get_history(session_id: str, limit: int = 10):
    with engine.begin() as conn:
        rows = conn.exec_driver_sql(
            "SELECT id, session_id, text, emotion, created_at FROM interactions WHERE session_id=? ORDER BY id DESC LIMIT ?",
            (session_id, limit)
        ).all()
    return [dict(r._mapping) for r in rows]
