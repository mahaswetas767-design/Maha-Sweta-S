# Phase 2 Review Report — Next 35% Milestone

## What was added
- Synthetic operational-risk ML benchmark using Random Forest.
- Model artifact and reproducible training script.
- Dashboard risk prediction with confidence and class probabilities.
- Rule-based recommendation + ML risk shown together so analysts can compare explainable evidence with a statistical benchmark.
- Analyst-study data collection template for novice vs experienced analysts.
- Reusable before/after evaluation metrics.
- Performance benchmark and ML error-analysis notes.
- Additional automated tests for the Phase 2 evaluation layer.

## Measured synthetic ML benchmark
The model is trained on a rule-generated synthetic target, not real incident labels. Therefore these numbers are engineering benchmark results only.

- Accuracy: 0.7317
- Weighted precision: 0.7354
- Weighted recall: 0.7317
- Weighted F1: 0.7282

## Error analysis
The confusion matrix shows that most errors occur between Low and Medium risk. High-risk recall is lower than the other classes because the synthetic High class is smaller. This is a reason to keep human confirmation and the original explainable rules in the workflow rather than allowing the model to make containment decisions.

## Human study status
No novice-vs-experienced human results are fabricated. `data/evaluation/analyst_sessions_template.csv` is ready for an approved study. The project records the required metrics: procedure adherence, missed steps, evidence completeness, decision accuracy, investigation time, and critical errors.

## Safety boundary
The ML model only provides a risk benchmark/prediction. It cannot isolate devices, block networks, disable accounts, or perform containment. High-impact actions remain simulation-only and require human confirmation.
