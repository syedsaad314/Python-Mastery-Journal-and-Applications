# Operational Instructions: Distributed Consensus Engine (Raft Initialization Track)

## 1. Environment Configurations
Ensure you are using python runtime engines matching specifications (Python >= 3.10). Initialize table rendering tools:
```bash
pip install -r requirements.txt
```

## 2. Running Simulations
Run the main validation script from your terminal:
```bash
python main.py
```

## 3. Key Telemetry Indicators to Watch
* **ELECTION_TIMEOUT_TRIGGERED**: Indicates a follower's timer expired, prompting it to increment the term counter and transition to a candidate.
* **VOTE_GRANTED**: Confirms a peer node has validated a candidate's credentials and cast a ballot for it.
* **LEADER_HEARTBEAT_BROADCAST**: Shows the newly elected leader broadcasting periodic heartbeats to maintain cluster alignment.