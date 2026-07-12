# Operational Instructions: Distributed Two-Phase Commit Transaction Engine

## 1. Environment Configuration
Ensure you are running a Python engine matching requirements (Python >= 3.10). Initialize reporting dependencies:
```bash
pip install -r requirements.txt
```

## 2. Running Simulations
Execute the orchestration harness to view transactional tracing:
```bash
python main.py
```

## 3. Key Telemetry Indicators to Watch
* **TRANSACTION_INITIATED**: Traced when a client kicks off a new cross-shard write request.
* **VOTE_REQUEST_SENT**: Confirms Phase 1 prepare commands have been dispatched to all participants.
* **PARTICIPANT_VOTED**: Logs individual node responses along with their local status votes.
* **GLOBAL_COMMIT_EXECUTED**: Confirms the transaction successfully achieved unanimous agreement and is being written across all shards.
* **GLOBAL_ABORT_TRIGGERED**: Indicates a node voted NO or timed out, causing the entire transaction to be safely rolled back.