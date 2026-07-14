# Operational Instructions: Asynchronous Orchestration Saga Engine

## 1. Environment Verification
Verify that your system runtime environment matches Python version 3.10 or higher.

## 2. Executing the System Harness
Run the master orchestration harness directly from your terminal:
```bash
python main.py
```

## 3. Telemetry Indicators to Monitor
* `[ORCHESTRATOR START]`: Emitted when a new distributed transaction context is initialized.
* `[FORWARD STEP]`: Fired when an action successfully updates a microservice.
* `[FAULT DETECTED]`: Flags a failure point, displaying the error message and stopping the forward chain.
* `[COMPENSATE RUN]`: Logs the reverse rollback steps as they undo previous mutations.