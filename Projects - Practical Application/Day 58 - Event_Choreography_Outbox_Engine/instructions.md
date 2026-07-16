# Operational Instructions: Choreographed Saga & Outbox Engine

## 1. Prerequisites Check
Ensure your execution terminal path uses Python version 3.10 or above.

## 2. Launching Verification Execution
Execute the driver engine from the project root using:
```bash
python main.py
```

## 3. Telemetry Indicators to Monitor
* `[OUTBOX COMMITTED]`: Local state mutation and outbox record written inside an atomic transaction block.
* `[BROKER ROUTING]`: Shows events being dispatched to decoupled microservices.
* `[CONSUMER PROCESSING]`: Verifies active event parsing alongside idempotency check guards.
* `[CHOREOGRAPHY ROLLBACK]`: Highlights decentralized compensations triggering automatically after a failure event.