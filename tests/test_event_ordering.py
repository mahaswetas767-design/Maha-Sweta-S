from src.engine.event_processor import EventProcessor
def test_out_of_order():
    p=EventProcessor()
    for x in [{"event_id":"E1","timestamp":"2026-01-01 10:01"},
              {"event_id":"E3","timestamp":"2026-01-01 10:03"},
              {"event_id":"E2","timestamp":"2026-01-01 10:02"}]: p.ingest(x)
    assert [x["event_id"] for x in p.ordered()]==["E1","E2","E3"]
