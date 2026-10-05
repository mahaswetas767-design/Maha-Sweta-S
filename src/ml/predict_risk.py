"""Predict synthetic operational risk for one SOC event."""
from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "risk_model.joblib"
CATEGORICAL = ["event_type", "device_type", "department", "authentication_status", "network_status", "malware_indicator", "protocol", "alert_source"]
NUMERIC = ["failed_login_count", "data_access_count"]
FEATURES = CATEGORICAL + NUMERIC

def predict(event):
    model = joblib.load(MODEL_PATH)
    row = pd.DataFrame([event])
    for col in CATEGORICAL:
        if col not in row:
            row[col] = "Unknown"
        row[col] = row[col].fillna("Unknown").astype(str)
    for col in NUMERIC:
        if col not in row:
            row[col] = 0
        row[col] = pd.to_numeric(row[col], errors="coerce").fillna(0)
    row = row[FEATURES]
    out = {"risk_level": str(model.predict(row)[0])}
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(row)[0]
        out["confidence"] = round(float(max(probs)), 4)
        out["class_probabilities"] = {str(c): round(float(p), 4) for c, p in zip(model.classes_, probs)}
    return out

if __name__ == "__main__":
    print(predict({"event_type": "Suspicious Network Connection", "device_type": "Patient Monitor", "department": "ICU", "authentication_status": "Failed", "network_status": "Degraded", "malware_indicator": "Suspected", "protocol": "TCP", "alert_source": "IDS", "failed_login_count": 7, "data_access_count": 30}))
