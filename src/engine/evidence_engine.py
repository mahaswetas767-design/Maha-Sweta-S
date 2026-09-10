from datetime import datetime, timezone
import uuid
class EvidenceEngine:
    def __init__(self):
        self.records=[]
    def add(self, investigation_id,event_id,evidence_type,description,analyst,source="SOC"):
        rec={"evidence_id":f"EVD-{uuid.uuid4().hex[:8].upper()}","investigation_id":investigation_id,
             "event_id":event_id,"evidence_type":evidence_type,"description":description,
             "timestamp":datetime.now(timezone.utc).isoformat(),"analyst":analyst,"source":source}
        self.records.append(rec); return rec
