# Phase 2 Performance Measurement

The application measures the time needed to process a batch of synthetic events and the ML prediction latency. Run:

```bash
python -m src.evaluation.benchmark
```

The generated `reports/performance_results.json` is a local engineering measurement. Hardware and Python/package versions affect the numbers, so it must not be presented as a production SLA.
