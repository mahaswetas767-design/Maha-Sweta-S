# Edge Case Test Results
The MVP includes automated tests for duplicate, out-of-order and override handling.

- Duplicate event: expected to be processed once.
- Out-of-order events: expected final logical ordering by timestamp.
- Delayed events: accepted by event ingestion and reflected when ordered.
- Override without reason: blocked.

Run `pytest` to reproduce the tests.
