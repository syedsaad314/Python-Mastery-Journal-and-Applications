# Operational Instructions: Distributed Gossip Membership Subsystem

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
* **GOSSIP_CYCLE_PROPAGATION**: Tracks nodes randomly selecting peers and infecting them with fresh heartbeat counters.
* **ANTI_ENTROPY_TRIGGER**: Logged during a full table comparison check, syncing nodes that have fallen behind.
* **CLUSTER_EVICTION_ALERT**: Shows failure detection logic changing an uncommunicative node's state from `ALIVE` to `DEAD`.