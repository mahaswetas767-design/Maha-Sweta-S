# Phase 2 ML Risk Model Results

A Random Forest classifier predicts a synthetic operational risk category from cleaned Hospital SOC event attributes.

**Important:** the target label is generated from transparent synthetic rules because there are no real incident ground-truth labels. Metrics are benchmark results, not clinical or production accuracy.

- Dataset rows: 2998
- Training rows: 2398
- Test rows: 600
- Accuracy: 0.7317
- Weighted precision: 0.7354
- Weighted recall: 0.7317
- Weighted F1: 0.7282

## Class distribution
```json
{
  "Low": 1921,
  "Medium": 901,
  "High": 176
}
```

## Confusion matrix
Order: Low, Medium, High.
```text
[[315, 69, 1], [59, 116, 5], [4, 23, 8]]
```

Model artifact: `models/risk_model.joblib`
