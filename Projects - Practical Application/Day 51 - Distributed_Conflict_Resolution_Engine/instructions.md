# Operational Instructions: Distributed Conflict Resolution Engine

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
* **CAUSAL_DOMINANCE_MUTATION**: Indicates a clean overwrite because the incoming write is strictly newer than the local record.
* **CONCURRENT_CONFLICT_DETECTED**: Flagged when divergent writes occur in parallel, triggering a multi-version sibling branch.
* **SIBLING_RECONCILIATION_MERGE**: Confirms that conflicting versions have been successfully merged into a unified history.