# Operational Instructions: Enterprise Concurrent Task Queue
**Author:** Syed Saad Bin Irfan

## 1. Environment Setup
Ensure you are using Python 3.10+ and install the versioned CLI presentation dependencies:
```bash
pip install -r requirements.txt
```

## 2. Running the Application
Launch the central orchestration engine to initialize the job queues, background threads, and terminal dashboard:

```Bash
python app_lifegiver.py
```

## 3. Verifying Operations
Observe the interactive CLI updates as the concurrent workers pull jobs from the priority queue.

View simulated task failures route automatically to the Dead-Letter Queue (DLQ) after their retry counts are exhausted.