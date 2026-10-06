# Hospital SOC Playbook Assistant — Phase 3 (Next 30%)

This folder contains the next implementation stage after the initial MVP.

## What this stage adds
- SQLite persistence
- Investigation/evidence/decision records
- Audit trail persistence
- Human-confirmation safety gate
- Mandatory override reason
- Evaluation metrics
- Analyst session template
- Dedicated Streamlit dashboard
- Automated tests

## Run
From the repository root:

```bash
pip install -r requirements.txt
streamlit run app/phase3_dashboard.py
```

## Test
```bash
pytest tests/test_phase3_metrics.py tests/test_phase3_persistence.py
```

## Important
All data is synthetic. This project is a cybersecurity decision-support simulation and does not control real medical devices or hospital systems.
