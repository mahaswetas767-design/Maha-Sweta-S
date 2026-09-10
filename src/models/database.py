from pathlib import Path
from sqlalchemy import create_engine
ROOT=Path(__file__).resolve().parents[2]
engine=create_engine(f"sqlite:///{ROOT/'soc_assistant.db'}",future=True)
def get_engine(): return engine
