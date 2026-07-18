# Operational Runbook: Event Sourcing & CQRS Coordination Engine

## 1. Prerequisites Verification
Verify that your terminal workspace environment uses Python 3.10 or higher.

## 2. Launching Core Engine
Execute the main system verification script from your terminal:
```bash
python main.py
```

## 3. Key Telemetry Indicators to Monitor
* `[COMMAND VALIDATED]`: The write-model successfully passes business invariants.
* `[EVENT APPENDED]`: The resulting change is saved as an immutable record in the append-only log.
* `[SNAPSHOT CHECKPOINT]`: A state snapshot is saved to optimize future lookups.
* `[PROJECTION SYNCED]`: The separate read-model updates instantly to match the new history.