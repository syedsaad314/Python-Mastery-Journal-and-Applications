# Enterprise Concurrent Task Queue and Background Job Scheduler Engine

An enterprise-grade, multi-threaded background task processing system built from scratch in Python. The system provides a lock-protected priority queue, a configurable background worker thread pool, automated error retry loops, and a dedicated Dead-Letter Queue (DLQ) for failed tasks—all monitored in real time via an interactive terminal dashboard.

## System Features

* **Thread-Safe Architecture:** Uses strict mutual-exclusion locks (`threading.Lock`) across all task extraction and submission paths to prevent race conditions.
* **Logarithmic Priority Ingestion:** Uses a binary heap implementation (`heapq`) to ensure high-priority tasks are scheduled and extracted efficiently in $O(\log N)$ time.
* **Fault-Tolerant Execution Guards:** Tracks worker execution, retrying failed tasks automatically before routing permanently broken items to the Dead-Letter Queue (DLQ) for isolation.
* **Real-Time CLI Dashboard:** Features a scannable, interactive terminal UI that tracks worker utilization, task counters, and error states using `tabulate` and `colorama`.

## Modular Architecture Overview

The system is split into distinct, single-responsibility modules:
* `job_model.py`: Defines task properties, priorities, and state boundaries.
* `queue_manager.py`: Manages the thread-safe priority heap and handles DLQ routing.
* `worker_pool.py`: Coordinates the lifecycle of background worker threads.
* `dashboard_ui.py`: Renders the live system status and metric tables in the terminal.
* `app_lifegiver.py`: The main orchestrator that schedules tasks and initializes the background pools.

## License

This project is open-source software licensed under the [MIT License](LICENSE).

***

**Lead Engineer:** Syed Saad Bin Irfan  
*Undergraduate Software Engineering Student | Certified Prompt Engineer*