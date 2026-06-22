# Operational Instructions: Replicated Key-Value Store System
**Lead Engineer:** Syed Saad Bin Irfan

## 1. Environment Verification
Ensure your local machine is running Python 3.10 or higher. Install the table formatting dependency:
```bash
pip install -r requirements.txt
```

## 2. Running the System
Run the main application script to simulate leader election, data writing, and consensus log replication across the cluster:

```Bash
python main.py
```
## 3. Operational Outcomes
Monitor the terminal output to watch cluster nodes run election cycles and vote for a leader.

Watch the log replication updates to see data commands replicate across followers and commit safely once a quorum is reached.