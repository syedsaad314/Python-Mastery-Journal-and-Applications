# Operational Instructions: Distributed Rate Limiter Engine
**Engineer:** Syed Saad Bin Irfan

## 1. Setup & Installation
Ensure you are using Python 3.10 or higher, then pull down the console visualization dependencies:
```bash
pip install -r requirements.txt

```
## 2. Core Execution Playbook
Run the central application script to initialize the simulated multi-node API cluster and view the real-time rate-limiting updates:

```Bash
python app_lifegiver.py
```

## 3. Telemetry Insights
Watch the live metrics update as burst traffic patterns simulate standard operations vs sudden traffic spikes.

Monitor how token consumption scales across individual API gateway nodes while synchronized cluster states are maintained.