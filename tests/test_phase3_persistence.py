from pathlib import Path
from src.persistence.sqlite_store import SQLiteStore

def test_sqlite_persistence(tmp_path: Path):
    store = SQLiteStore(tmp_path / "test.db")
    store.add_investigation("INV-T", "Open", "A1", "2026-10-06T10:00:00")
    store.add_evidence("INV-T", "EVT-T", "log", "synthetic evidence", "A1", "test", "2026-10-06T10:01:00")
    store.add_decision("INV-T", "Investigate", "Review", "accept", "", False, "2026-10-06T10:02:00")
    store.add_audit("INV-T", "test", "ok", "2026-10-06T10:02:00")
    counts = store.counts()
    assert counts["investigations"] == 1
    assert counts["evidence"] == 1
    assert counts["decisions"] == 1
    assert counts["audit_log"] == 1
    store.close()

def test_override_requires_reason(tmp_path: Path):
    store = SQLiteStore(tmp_path / "test.db")
    try:
        store.add_decision("INV-T", "Investigate", "Review", "override", "", False, "now")
        assert False, "Expected ValueError"
    except ValueError:
        pass
    finally:
        store.close()
