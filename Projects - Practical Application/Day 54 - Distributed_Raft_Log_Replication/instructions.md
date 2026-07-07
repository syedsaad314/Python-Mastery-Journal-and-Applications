# Operational Instructions: Distributed Consensus Log Replication Engine

## 1. Environment Configurations
Ensure you are running a Python engine matching standard requirements (Python >= 3.10). Initialize visual monitoring tools:
```bash
pip install -r requirements.txt
```

## 2. Running Simulations
Execute the orchestration harness to trace consensus operations across our mock cluster:
```bash
python main.py
```

## 3. Key Telemetry Indicators to Watch
* **LOG_REPLICATION_REQUESTED**: Traced when a client request hits the leader, triggering a write to its local log.
* **LOG_MATCHING_FAILED**: Logged when a follower rejects an update due to an index or term mismatch.
* **COMMIT_INDEX_ADVANCED**: Confirms an entry has achieved a cluster majority and is safe to finalize.
* **STATE_MACHINE_APPLIED**: Traced when a verified command is safely executed by the storage engine.