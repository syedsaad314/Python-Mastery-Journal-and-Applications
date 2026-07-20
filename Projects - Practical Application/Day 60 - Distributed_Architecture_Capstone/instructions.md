# Operational Instructions: Comprehensive Architecture Capstone

## 1. System Runtime Verification
Ensure your terminal environment path matches Python version 3.10 or higher.

## 2. Executing the Complete Simulation Suite
Run the master benchmarking and fault-injection dashboard using:
```bash
python main.py
```

## 3. High-Fidelity Observability Indicators to Monitor
* `[ORCHESTRATOR INJECT]`: Central conductor detects a microservice error and triggers a backward rollback.
* `[CHOREOGRAPHY INJECT]`: Autonomous services catch a failure event and run local rollbacks independently.
* `[OUTBOX STAGE]`: Updates saved together safely inside an atomic transaction block.
* `[OCC COLLISION BLOCK]`: Optimistic concurrency control blocks simultaneous conflicting writes.
* `[SNAPSHOT SPEEDUP]`: Shows the exact speed gains achieved by restoring state via checkpoints.