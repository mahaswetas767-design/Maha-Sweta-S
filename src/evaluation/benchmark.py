"""Measure local synthetic event-processing and ML prediction latency."""
from pathlib import Path
import json, time
import pandas as pd
from src.engine.event_processor import EventProcessor
from src.ml.predict_risk import predict

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cleaned" / "hospital_soc_events_cleaned.csv"
OUT = ROOT / "reports" / "performance_results.json"

def main():
    df = pd.read_csv(DATA).head(250)
    processor = EventProcessor()
    t0 = time.perf_counter()
    for row in df.to_dict("records"):
        processor.ingest(row)
    event_ms = (time.perf_counter() - t0) * 1000
    sample = df.iloc[0].to_dict()
    # Warm-up load happens on the first call; report it separately from a repeated prediction.
    t1 = time.perf_counter(); predict(sample); first_ms = (time.perf_counter() - t1) * 1000
    t2 = time.perf_counter();
    for _ in range(20): predict(sample)
    repeat_ms = (time.perf_counter() - t2) * 1000 / 20
    result = {
        "events_processed": int(len(df)),
        "event_processing_total_ms": round(event_ms, 3),
        "ml_first_prediction_ms": round(first_ms, 3),
        "ml_repeated_prediction_avg_ms": round(repeat_ms, 3),
        "note": "Local synthetic benchmark; hardware/package dependent; not a production SLA."
    }
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
