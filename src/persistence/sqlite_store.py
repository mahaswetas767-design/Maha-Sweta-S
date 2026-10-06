from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Dict, Iterable, Optional

DEFAULT_DB = Path("data") / "hospital_soc_phase3.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS investigations (
    investigation_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    current_step INTEGER DEFAULT 1,
    analyst_id TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id TEXT NOT NULL,
    event_id TEXT,
    evidence_type TEXT,
    description TEXT,
    analyst TEXT,
    source TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decisions (
    decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id TEXT NOT NULL,
    action TEXT NOT NULL,
    recommendation TEXT,
    analyst_decision TEXT,
    override_reason TEXT,
    human_confirmed INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT,
    created_at TEXT NOT NULL
);
"""

class SQLiteStore:
    def __init__(self, db_path: str | Path = DEFAULT_DB):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def add_investigation(self, investigation_id: str, status: str, analyst_id: str, created_at: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO investigations(investigation_id,status,current_step,analyst_id,created_at) VALUES(?,?,?,?,?)",
            (investigation_id, status, 1, analyst_id, created_at),
        )
        self.conn.commit()

    def add_evidence(self, investigation_id: str, event_id: str, evidence_type: str,
                     description: str, analyst: str, source: str, created_at: str) -> None:
        self.conn.execute(
            """INSERT INTO evidence(investigation_id,event_id,evidence_type,description,analyst,source,created_at)
               VALUES(?,?,?,?,?,?,?)""",
            (investigation_id, event_id, evidence_type, description, analyst, source, created_at),
        )
        self.conn.commit()

    def add_decision(self, investigation_id: str, action: str, recommendation: str,
                     analyst_decision: str, override_reason: str = "",
                     human_confirmed: bool = False, created_at: str = "") -> None:
        if analyst_decision == "override" and not override_reason.strip():
            raise ValueError("Override reason is required.")
        self.conn.execute(
            """INSERT INTO decisions(investigation_id,action,recommendation,analyst_decision,
                                      override_reason,human_confirmed,created_at)
               VALUES(?,?,?,?,?,?,?)""",
            (investigation_id, action, recommendation, analyst_decision,
             override_reason, int(human_confirmed), created_at),
        )
        self.conn.commit()

    def add_audit(self, investigation_id: str, action: str, details: str, created_at: str) -> None:
        self.conn.execute(
            "INSERT INTO audit_log(investigation_id,action,details,created_at) VALUES(?,?,?,?)",
            (investigation_id, action, details, created_at),
        )
        self.conn.commit()

    def counts(self) -> Dict[str, int]:
        out = {}
        for table in ("investigations", "evidence", "decisions", "audit_log"):
            out[table] = self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        return out

    def close(self):
        self.conn.close()
