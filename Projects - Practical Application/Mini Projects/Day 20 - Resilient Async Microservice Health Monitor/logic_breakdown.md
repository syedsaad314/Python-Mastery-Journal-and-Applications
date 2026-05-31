# Portfolio Code Review: Resilient Async Microservice Health Monitor
**Engineer:** Syed Saad Bin Irfan

## The Problem
Legacy, synchronous monitoring systems verify endpoints sequentially. If multiple servers time out, delays pile up, which stalls data collection dashboards and delays critical system alerts.

## Engineering Standards Applied
* **Concurrent Endpoint Probing:** Uses `asyncio.gather` to request metrics from all service nodes simultaneously. This structure ensures total evaluation times stay bound to the single longest network timeout delay, rather than stacking sequentially.
* **Granular Network Exception Safety:** Uses structured `asyncio.wait_for` wrappers to trap `TimeoutError` exceptions cleanly. This prevents unresponsive target servers from blocking upstream processing pipelines.
* **Async Mutex Resource Controls:** Protects the shared metrics dictionary with an `asyncio.Lock()` block, ensuring memory updates stay consistent and preventing coroutine race conditions.