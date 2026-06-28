# Operational Instructions: Distributed Consistent Hash Subsystem

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
* **MAPPED_PRIMARY**: Shows the primary node responsible for handling the target key.
* **BOUNDED_LOAD_REALLOCATION**: Indicates when a request is forwarded to a fallback node due to capacity limits.
* **REPLICA_CHAIN**: Confirms that data replicas are placed across distinct physical nodes.