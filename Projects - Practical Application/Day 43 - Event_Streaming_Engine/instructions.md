# Operational Instructions: Distributed Event Streaming Engine
**Lead Engineer:** Syed Saad Bin Irfan

## 1. Environment Setup
Verify that your machine is running Python 3.10+ and pull down the formatting packages:
```bash
pip install -r requirements.txt
```

## 2. Core Execution Playbook
Launch the central engine using the orchestration script to start the message brokers, partition routers, and background consumers:

```Bash
python app_lifegiver.py
```

## 3. Operational Insights
Watch the live metrics update as producers distribute financial transaction events evenly across multiple topic partitions.

Monitor how worker consumer threads process events in parallel and safely commit their offset checkpoints.