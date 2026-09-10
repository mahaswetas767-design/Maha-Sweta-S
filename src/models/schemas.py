from pydantic import BaseModel
class OverrideRequest(BaseModel):
    investigation_id:str
    recommendation:str
    decision:str
    reason:str
    analyst_id:str="analyst_demo"
class EvidenceRequest(BaseModel):
    investigation_id:str
    event_id:str
    evidence_type:str
    description:str
    analyst:str="analyst_demo"
