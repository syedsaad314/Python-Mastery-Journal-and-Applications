# Portfolio Code Review: Async Service Prober
**Author:** Syed Saad Bin Irfan

## Practical Context
This monitoring script is designed to track microservice infrastructure health cleanly and concurrently without blocking execution loops.

## Engineering Standards Applied
* **Concurrency Model:** Leverages Python's single-threaded `asyncio` loop to execute tasks concurrently, avoiding the heavy memory overhead of running multiple native OS threads.
* **Network Fault Tolerance:** Implements an elegant retry fallback mechanism that attempts to reconnect to a failing node before officially flagging it as offline.
* **Performance Profile:** Runs network sweeps in parallel; the total execution time is bounded by the single slowest active node rather than the cumulative sum of all node response times combined.