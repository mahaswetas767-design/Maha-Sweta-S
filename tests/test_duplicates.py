from src.engine.event_processor import EventProcessor
def test_duplicate_ignored():
    p=EventProcessor()
    x={"event_id":"E1","timestamp":"2026-01-01 10:01"}
    assert p.ingest(x) is True
    assert p.ingest(x) is False
