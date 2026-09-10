class EventProcessor:
    """Deduplicates by event_id and exposes events in logical timestamp order."""
    def __init__(self):
        self.events={}
    def ingest(self,event):
        eid=event["event_id"]
        if eid in self.events:
            return False
        self.events[eid]=event
        return True
    def ordered(self):
        return sorted(self.events.values(),key=lambda x:x["timestamp"])
