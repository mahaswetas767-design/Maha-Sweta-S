"""Generate synthetic hospital SOC events."""
from pathlib import Path
import random
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[2] / "data" / "raw" / "hospital_soc_events_raw.csv"
# Dataset is committed with the repository; this script can be replaced by a larger generator.
def main():
    print(f"Raw dataset available at: {OUT}")
    print(pd.read_csv(OUT).shape)
if __name__ == "__main__":
    main()
