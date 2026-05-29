# Logic Breakdown: Custom Thread Pools via Queues
**Engineer:** Syed Saad Bin Irfan

## The Problem
Spawning and destroying native threads repeatedly is expensive due to OS context allocation overhead. For high-volume tasks, threads should be created once and reused throughout the application lifecycle.

## My Approach
I engineered a custom thread pool utilizing a thread-safe `queue.Queue`. 

The pool initializes a fixed number of worker threads that run continuously. These threads pull tasks from the queue using blocking `.get()` operations, execute the assigned functions, and wait for the next task. To shut down the pool cleanly, I implemented a sentinel object pattern that signals the worker loops to exit safely.

## Complexity Profile
* **Runtime Bounds:** Task ingestion runs in $O(1)$ time, while worker distribution scales at $O(T / W)$.
* **Space Constraints:** Keeps thread overhead capped at a flat $O(W)$ resource footprint.