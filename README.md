# MedSecure Hospital SOC Investigation Playbook Assistant

## 35% MVP

A defensive cybersecurity application that guides junior SOC analysts through approved hospital investigation procedures using explainable rules, evidence recording, human confirmation, manual override and an auditable decision trail.

**All data is synthetic. Containment actions are simulation-only.**

## Features
- Synthetic raw and cleaned SOC datasets
- Data preprocessing and IQR outlier handling
- Explainable rule-based recommendations
- Investigation/evidence workflow
- Human confirmation for high-impact actions
- Mandatory override reason
- Audit trail
- Duplicate and out-of-order event handling
- Streamlit SOC dashboard
- Pytest edge-case tests

## Run
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
pip install -r requirements.txt
python src/data/preprocess.py
streamlit run app/dashboard.py
```

Run tests:
```bash
pytest
```

## Architecture
Raw SOC events → preprocessing → event processor → explainable rules → playbook guidance → evidence → human decision/override → audit trail → dashboard.

## Safety
This is a local research/training prototype. It must not be connected to real medical devices or used for automatic containment.

## Phase 2
- Approved user study comparing novice and experienced analysts
- ML/DL performance comparison
- GenAI/RAG assistant
- Vector database
- Real SIEM integration
- Authentication and RBAC
- Production deployment
- Advanced analytics and stakeholder validation
