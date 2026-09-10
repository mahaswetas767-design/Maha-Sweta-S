class PlaybookEngine:
    def __init__(self, steps):
        self.steps=steps
        self.current=0
        self.completed=[]
    @property
    def current_step(self):
        return self.steps[self.current] if self.current < len(self.steps) else "Completed"
    def complete_step(self):
        if self.current < len(self.steps):
            self.completed.append(self.steps[self.current]); self.current+=1
        return self.current_step
