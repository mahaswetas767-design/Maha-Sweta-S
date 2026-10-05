# MedSecure Hospital SOC Investigation Playbook Assistant

## Phase 2 — Next 35% Review Build

A defensive cybersecurity research prototype for hospital SOC investigation support. The Phase 1 foundation is extended with a **synthetic ML risk benchmark, model evaluation, dashboard integration, analyst-study measurement framework, performance measurement, and error analysis**.

**All data is synthetic. This system is simulation-only and must not control real medical devices or automatically perform containment.**

## Phase 2 additions
- Random Forest operational-risk benchmark using scikit-learn.
- Reproducible model training and saved `models/risk_model.joblib`.
- ML prediction and confidence shown inside the Streamlit dashboard.
- Rule-based recommendations remain visible beside ML output for explainability.
- Model card and error-analysis report.
- Analyst-session template for an approved novice vs experienced study.
- Reusable before/after evaluation metrics.
- Local event/ML performance benchmark.
- Additional automated evaluation test.

## Run
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
pip install -r requirements.txt
python src/data/preprocess.py
python src/ml/train_risk_model.py
streamlit run app/dashboard.py
```

Run tests:
```bash
pytest
```

Optional performance benchmark:
```bash
python -m src.evaluation.benchmark
```

## Architecture
Raw SOC events → preprocessing → event processor → explainable rules → ML risk benchmark → playbook guidance → evidence → human decision/override → audit trail → dashboard → evaluation framework.

## Evaluation boundary
The included ML metrics are **synthetic engineering benchmarks** because the target label is generated from transparent rules. No novice-vs-experienced human study results are fabricated. The analyst template must be populated only after an approved study.

## Safety
- No patient-identifying information.
- No real hospital/SIEM integration.
- No automatic containment.
- High-impact actions require human confirmation.
- Manual overrides require a reason and are recorded.
- ML output is advisory and cannot trigger medical-device actions.

## Not implemented yet
Production SIEM integration, real medical-device control, cloud deployment, authentication/RBAC, RAG/vector database, advanced deep learning, and formal human-subject study deployment remain outside this milestone.
