"""Train a synthetic SOC operational-risk classifier."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "cleaned" / "hospital_soc_events_cleaned.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "risk_model.joblib"
METRICS_PATH = ROOT / "reports" / "ml_results.json"
REPORT_PATH = ROOT / "reports" / "ml_results.md"
CATEGORICAL = ["event_type", "device_type", "department", "authentication_status", "network_status", "malware_indicator", "protocol", "alert_source"]
NUMERIC = ["failed_login_count", "data_access_count"]
FEATURES = CATEGORICAL + NUMERIC

def make_risk_label(df):
    score = np.zeros(len(df), dtype=int)
    score += df["severity"].map({"Low":0,"Medium":1,"High":2,"Critical":3}).fillna(1).to_numpy()
    score += (pd.to_numeric(df["failed_login_count"], errors="coerce").fillna(0) >= 5).astype(int).to_numpy()
    score += (pd.to_numeric(df["data_access_count"], errors="coerce").fillna(0) >= 80).astype(int).to_numpy()
    score += df["malware_indicator"].isin(["Detected","Suspected"]).astype(int).to_numpy() * 2
    score += df["event_type"].isin(["Privilege Escalation","Suspicious Network Connection"]).astype(int).to_numpy() * 2
    return pd.Series(np.where(score >= 5, "High", np.where(score >= 3, "Medium", "Low")), index=df.index, name="risk_label")

def main():
    df = pd.read_csv(DATA)
    df[NUMERIC] = df[NUMERIC].apply(pd.to_numeric, errors="coerce").fillna(0)
    df[CATEGORICAL] = df[CATEGORICAL].fillna("Unknown").astype(str)
    y = make_risk_label(df)
    X = df[FEATURES]
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),("num","passthrough",NUMERIC)])
    model = Pipeline([("preprocessor",pre),("classifier",RandomForestClassifier(n_estimators=150,random_state=42,class_weight="balanced"))])
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=42,stratify=y)
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    labels=["Low","Medium","High"]
    metrics={"experiment":"Synthetic SOC operational risk classification","label_definition":"Rule-generated benchmark label; not real-world or clinical ground truth","rows":int(len(df)),"train_rows":int(len(X_train)),"test_rows":int(len(X_test)),"accuracy":round(float(accuracy_score(y_test,pred)),4),"precision_weighted":round(float(precision_score(y_test,pred,average="weighted",zero_division=0)),4),"recall_weighted":round(float(recall_score(y_test,pred,average="weighted",zero_division=0)),4),"f1_weighted":round(float(f1_score(y_test,pred,average="weighted",zero_division=0)),4),"labels":labels,"confusion_matrix":confusion_matrix(y_test,pred,labels=labels).tolist(),"class_distribution":y.value_counts().to_dict()}
    joblib.dump(model,MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics,indent=2))
    REPORT_PATH.write_text(f"""# Phase 2 ML Risk Model Results\n\nA Random Forest classifier predicts a synthetic operational risk category from cleaned Hospital SOC event attributes.\n\n**Important:** the target label is generated from transparent synthetic rules because there are no real incident ground-truth labels. Metrics are benchmark results, not clinical or production accuracy.\n\n- Dataset rows: {metrics["rows"]}\n- Training rows: {metrics["train_rows"]}\n- Test rows: {metrics["test_rows"]}\n- Accuracy: {metrics["accuracy"]}\n- Weighted precision: {metrics["precision_weighted"]}\n- Weighted recall: {metrics["recall_weighted"]}\n- Weighted F1: {metrics["f1_weighted"]}\n\n## Class distribution\n```json\n{json.dumps(metrics["class_distribution"],indent=2)}\n```\n\n## Confusion matrix\nOrder: Low, Medium, High.\n```text\n{metrics["confusion_matrix"]}\n```\n\nModel artifact: `models/risk_model.joblib`\n""")
    print(json.dumps(metrics,indent=2))

if __name__ == "__main__": main()
