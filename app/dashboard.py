import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
import plotly.express as px
from src.engine.recommendation_engine import recommend
from src.engine.event_processor import EventProcessor
from src.engine.evidence_engine import EvidenceEngine
from src.engine.decision_logger import DecisionLogger

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/cleaned/hospital_soc_events_cleaned.csv"

st.set_page_config(page_title="MedSecure SOC Assistant",page_icon="🛡️",layout="wide")
st.title("🛡️ MedSecure SOC Investigation Assistant")
st.caption("Explainable investigation guidance for hospital cybersecurity operations • SYNTHETIC DATA • SIMULATION ONLY")

df=pd.read_csv(DATA)
processor=EventProcessor()
for _,r in df.head(500).iterrows(): processor.ingest(r.to_dict())

if "evidence" not in st.session_state: st.session_state.evidence=EvidenceEngine()
if "audit" not in st.session_state: st.session_state.audit=DecisionLogger()

page=st.sidebar.radio("Navigation",["Executive Overview","Investigation Workspace","Audit Trail","Edge Case Monitoring"])

if page=="Executive Overview":
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total Events",len(df))
    c2.metric("Critical Alerts",int((df.severity=="Critical").sum()))
    c3.metric("High Alerts",int((df.severity=="High").sum()))
    c4.metric("Unique Devices",df.device_id.nunique())
    col1,col2=st.columns(2)
    with col1:
        fig=px.bar(df["severity"].value_counts().reset_index(),x="severity",y="count",title="Events by Severity")
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        fig=px.pie(df,names="device_type",title="Events by Device Type")
        st.plotly_chart(fig,use_container_width=True)
    st.subheader("Recent Security Events")
    st.dataframe(df.head(20),use_container_width=True)

elif page=="Investigation Workspace":
    st.subheader("Investigation Workspace")
    idx=st.number_input("Select event row",0,max(0,min(499,len(df)-1)),0)
    event=df.iloc[int(idx)].to_dict()
    st.write(f"**Event:** {event['event_id']} | **Device:** {event['device_id']} | **Severity:** {event['severity']}")
    st.json({k:event[k] for k in ["event_id","event_type","device_type","department","user_id","source_ip","timestamp","failed_login_count","data_access_count"]})
    recs=recommend(event)
    st.subheader("Explainable Recommendations")
    if not recs: st.info("No rule triggered.")
    for rec in recs:
        with st.expander(f"{rec['rule_id']} — {rec['recommendation']}",expanded=True):
            st.write("**WHY:**",rec["reason"])
            st.write("**EVIDENCE:**"); st.json(rec["evidence"])
            st.write("**Human confirmation:**", "Required" if rec["requires_human_confirmation"] else "Not required")
            if rec["requires_human_confirmation"]:
                st.warning("SIMULATION ONLY — HUMAN APPROVAL REQUIRED")
                a,b,c=st.columns(3)
                if a.button("Approve",key="a"+rec["rule_id"]):
                    st.session_state.audit.log(event["investigation_id"],"High-impact approval",rec["recommendation"],"Approved",
                                               evidence_ids=[event["event_id"]])
                    st.success("Approval recorded in audit trail.")
                if b.button("Reject",key="r"+rec["rule_id"]):
                    st.session_state.audit.log(event["investigation_id"],"High-impact decision",rec["recommendation"],"Rejected",
                                               evidence_ids=[event["event_id"]])
                    st.info("Rejection recorded.")
                if c.button("Override",key="o"+rec["rule_id"]):
                    reason=st.text_input("Override reason",key="reason"+rec["rule_id"])
                    if st.button("Save Override",key="s"+rec["rule_id"]):
                        if not reason.strip(): st.error("Override reason is mandatory.")
                        else:
                            st.session_state.audit.log(event["investigation_id"],"Recommendation override",
                                rec["recommendation"],"Overridden",reason,[event["event_id"]],True)
                            st.success("Override recorded.")
    st.subheader("Add Evidence")
    desc=st.text_area("Evidence description")
    if st.button("Record Evidence"):
        if desc.strip():
            ev=st.session_state.evidence.add(event["investigation_id"],event["event_id"],"Analyst Note",desc,"analyst_demo")
            st.success(f"Evidence {ev['evidence_id']} recorded.")
        else: st.error("Evidence description required.")

elif page=="Audit Trail":
    st.subheader("Auditable Decision Trail")
    if st.session_state.audit.logs: st.dataframe(pd.DataFrame(st.session_state.audit.logs),use_container_width=True)
    else: st.info("No decisions recorded in this session yet.")
    st.subheader("Evidence")
    if st.session_state.evidence.records: st.dataframe(pd.DataFrame(st.session_state.evidence.records),use_container_width=True)
    else: st.info("No evidence recorded in this session yet.")

else:
    st.subheader("Edge Case Monitoring")
    st.write("The event processor deduplicates event IDs and sorts accepted events by timestamp.")
    sample=[{"event_id":"E1","timestamp":"2026-01-01 10:01:00"},
            {"event_id":"E3","timestamp":"2026-01-01 10:03:00"},
            {"event_id":"E2","timestamp":"2026-01-01 10:02:00"},
            {"event_id":"E3","timestamp":"2026-01-01 10:03:00"}]
    p=EventProcessor()
    results=[p.ingest(x) for x in sample]
    st.write("Accepted sequence:",results)
    st.write("Logical order:",[x["event_id"] for x in p.ordered()])
    st.success("Expected: duplicate E3 is ignored; final order is E1 → E2 → E3.")
