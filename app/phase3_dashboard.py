from __future__ import annotations
from datetime import datetime
from pathlib import Path
import sys
import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.persistence.sqlite_store import SQLiteStore
from src.evaluation.metrics import procedure_adherence, evidence_completeness, critical_error_rate

st.set_page_config(page_title="Hospital SOC - Phase 3", layout="wide")
st.title("Hospital SOC Investigation Playbook Assistant")
st.caption("Phase 3 (next 30%) — persistence, evaluation, analyst workflow and auditability. Simulation only.")

store = SQLiteStore()
page = st.sidebar.radio(
    "Navigation",
    ["Operational Dashboard", "Investigation Record", "Evidence & Decision", "Evaluation"]
)

if page == "Operational Dashboard":
    st.subheader("Persistent system status")
    counts = store.counts()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Investigations", counts["investigations"])
    c2.metric("Evidence", counts["evidence"])
    c3.metric("Decisions", counts["decisions"])
    c4.metric("Audit Entries", counts["audit_log"])
    st.info("High-impact actions remain human-confirmed and simulation-only.")

elif page == "Investigation Record":
    st.subheader("Create / update investigation")
    inv = st.text_input("Investigation ID", "INV-001")
    analyst = st.text_input("Analyst ID", "ANALYST-001")
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    if st.button("Save Investigation"):
        store.add_investigation(inv, status, analyst, datetime.now().isoformat(timespec="seconds"))
        store.add_audit(inv, "investigation_saved", f"status={status}", datetime.now().isoformat(timespec="seconds"))
        st.success("Investigation saved to SQLite.")

elif page == "Evidence & Decision":
    st.subheader("Evidence")
    inv = st.text_input("Investigation ID", "INV-001")
    event = st.text_input("Event ID", "EVT-001")
    desc = st.text_area("Evidence description", "Synthetic evidence recorded for investigation.")
    if st.button("Save Evidence"):
        store.add_evidence(inv, event, "SOC event", desc, "ANALYST-001", "synthetic dataset",
                           datetime.now().isoformat(timespec="seconds"))
        store.add_audit(inv, "evidence_added", event, datetime.now().isoformat(timespec="seconds"))
        st.success("Evidence saved.")

    st.divider()
    st.subheader("Decision")
    action = st.selectbox("Action", ["Investigate", "Escalate Incident", "Isolate Device", "Block Network", "Disable Account"])
    recommendation = st.text_input("System recommendation", "Review evidence and follow approved playbook.")
    decision = st.selectbox("Analyst decision", ["accept", "reject", "override"])
    reason = st.text_area("Override reason (required for override)")
    confirmed = st.checkbox("Human confirmation provided for high-impact action")
    if st.button("Save Decision"):
        high_impact = action in {"Escalate Incident", "Isolate Device", "Block Network", "Disable Account"}
        if high_impact and not confirmed:
            st.error("Human confirmation is required for this high-impact action.")
        elif decision == "override" and not reason.strip():
            st.error("Override reason is required.")
        else:
            store.add_decision(inv, action, recommendation, decision, reason, confirmed,
                               datetime.now().isoformat(timespec="seconds"))
            store.add_audit(inv, "decision_saved", f"{action}:{decision}",
                            datetime.now().isoformat(timespec="seconds"))
            st.success("Decision and audit entry saved.")

else:
    st.subheader("Evaluation metrics")
    st.caption("These controls calculate metrics; they do not fabricate a real analyst study.")
    c1, c2, c3 = st.columns(3)
    completed = c1.number_input("Completed playbook steps", min_value=0, value=9)
    expected = c2.number_input("Expected playbook steps", min_value=1, value=10)
    captured = c3.number_input("Evidence items captured", min_value=0, value=8)
    required = st.number_input("Required evidence items", min_value=1, value=10)
    errors = st.number_input("Critical errors", min_value=0, value=1)
    cases = st.number_input("Total cases", min_value=1, value=20)
    a, b, c = st.columns(3)
    a.metric("Procedure adherence", f"{procedure_adherence(completed, expected):.1f}%")
    b.metric("Evidence completeness", f"{evidence_completeness(required, captured):.1f}%")
    c.metric("Critical error rate", f"{critical_error_rate(errors, cases):.1f}%")
