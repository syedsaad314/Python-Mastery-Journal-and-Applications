# Operational Instructions: Distributed Linearizable Read Subsystem

## 1. Dependency Configurations
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
* **LOCAL_LEASE_READ**: Indicates high-speed lookups served directly from memory while the lease is valid.
* **QUORUM_READ_INDEX_FALLBACK**: Shows the system falling back to consensus checks when the lease expires.
* **IDEMPOTENT CACHE HIT**: Confirms that retried client operations are safely deduplicated.