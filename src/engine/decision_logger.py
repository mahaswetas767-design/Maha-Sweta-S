from datetime import datetime, timezone
import uuid
class DecisionLogger:
    def __init__(self):
        self.logs=[]
    def log(self, investigation_id, action, system_recommendation, analyst_decision,
            reason="", evidence_ids=None, override=False, previous_state="", new_state=""):
        if override and not reason.strip():
            raise ValueError("Override reason is required.")
        rec={"audit_id":f"AUD-{uuid.uuid4().hex[:8].upper()}",
             "investigation_id":investigation_id,"timestamp":datetime.now(timezone.utc).isoformat(),
             "action":action,"system_recommendation":system_recommendation,
             "analyst_decision":analyst_decision,"reason":reason,
             "evidence_ids":evidence_ids or [],"override":override,
             "previous_state":previous_state,"new_state":new_state}
        self.logs.append(rec); return rec
