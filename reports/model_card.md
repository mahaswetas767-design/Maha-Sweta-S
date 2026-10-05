# Model Card — Synthetic SOC Risk Benchmark

**Model:** Random Forest classifier inside a scikit-learn pipeline  
**Purpose:** benchmark whether a simple ML model can classify synthetic operational risk.  
**Data:** synthetic hospital SOC events only.  
**Target:** Low / Medium / High operational risk generated from transparent rules.  
**Not a clinical model:** the labels are not medical outcomes and the model is not validated for real hospitals.

## Features
Categorical event/device/security telemetry plus failed-login and data-access counts.

## Benchmark
- Accuracy: 0.7317
- Weighted precision: 0.7354
- Weighted recall: 0.7317
- Weighted F1: 0.7282

## Limitations
- Synthetic labels can make the benchmark optimistic or unrepresentative.
- Class imbalance reduces reliability for the High class.
- No real hospital/SIEM validation was performed.
- Predictions must not trigger automatic containment.
