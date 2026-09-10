from pathlib import Path
import pandas as pd
import numpy as np
from ipaddress import ip_address

ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/"data/raw/hospital_soc_events_raw.csv"
CLEAN=ROOT/"data/cleaned/hospital_soc_events_cleaned.csv"
REPORT=ROOT/"reports/data_quality_report.md"

def valid_ip(x):
    try: ip_address(str(x)); return True
    except ValueError: return False

def preprocess():
    df=pd.read_csv(RAW)
    raw_rows, raw_cols=df.shape
    df=df.drop_duplicates().copy()
    duplicate_rows=raw_rows-len(df)
    for c in df.select_dtypes(include="object").columns:
        df[c]=df[c].astype("string").str.strip()
    df["event_type"]=df["event_type"].str.title()
    df["device_type"]=df["device_type"].str.title()
    df["severity"]=df["severity"].str.title()
    df["timestamp"]=pd.to_datetime(df["timestamp"],errors="coerce")
    df["failed_login_count"]=pd.to_numeric(df["failed_login_count"],errors="coerce")
    df["data_access_count"]=pd.to_numeric(df["data_access_count"],errors="coerce")
    invalid_ip=(~df["source_ip"].map(valid_ip)) | (~df["destination_ip"].map(valid_ip))
    df.loc[invalid_ip,["source_ip","destination_ip"]]=np.nan
    df.loc[df["failed_login_count"]<0,"failed_login_count"]=np.nan
    df.loc[df["data_access_count"]<0,"data_access_count"]=np.nan
    for c in ["failed_login_count","data_access_count"]:
        med=df[c].median()
        df[c]=df[c].fillna(med)
    df["severity"]=df["severity"].where(df["severity"].isin(["Low","Medium","High","Critical"]),"Medium")
    df=df.dropna(subset=["event_id","device_id","timestamp"]).copy()
    df=df.sort_values("timestamp").reset_index(drop=True)
    outliers={}
    for c in ["failed_login_count","data_access_count"]:
        q1,q3=df[c].quantile([.25,.75]); iqr=q3-q1
        mask=(df[c]<q1-1.5*iqr)|(df[c]>q3+1.5*iqr)
        outliers[c]=int(mask.sum())
        df.loc[mask,c]=df[c].clip(q1-1.5*iqr,q3+1.5*iqr)
    df["timestamp"]=df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    CLEAN.parent.mkdir(exist_ok=True)
    df.to_csv(CLEAN,index=False)
    report=f"""# Data Quality Report
- Raw rows: {raw_rows}
- Raw columns: {raw_cols}
- Cleaned rows: {len(df)}
- Cleaned columns: {df.shape[1]}
- Duplicate rows removed: {duplicate_rows}
- Missing/invalid values handled: numeric, IP, timestamp, IDs and severity
- IQR outliers handled: {outliers}
"""
    REPORT.write_text(report,encoding="utf-8")
    return df

if __name__=="__main__":
    preprocess()
