# Operational Instructions: Distributed Consensus Snapshot Compaction Engine

## 1. Environment Configuration
Ensure you use a Python runtime matching specifications (Python >= 3.10). Install reporting components:
```bash
pip install -r requirements.txt
```

## 2. Running Simulations
Execute the runner file to trace log compaction and `InstallSnapshot` operations across the cluster:
```bash
python main.py
```

## 3. Key Telemetry Indicators to Watch
* **LOG_COMPACTION_TRIGGERED**: Traced when a node reaches its log threshold and shrinks its history array.
* **SNAPSHOT_RPC_BROADCAST**: Logs when a leader encounters a lagging node and switches from sending standard log updates to an `InstallSnapshot` payload.
* **FOLLOWER_SNAPSHOT_INSTALLED**: Confirms a peer has successfully processed a snapshot and fast-forwarded its internal state.