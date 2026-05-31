# Logic Breakdown: Multi-Producer Multi-Consumer IPC Queues
**Engineer:** Syed Saad Bin Irfan

## The Problem
Pipes are excellent for simple, point-to-point connections, but they break down when managing complex data distribution patterns across multiple concurrent worker processes.

## My Approach
I implemented a multi-worker coordination design using a process-safe `multiprocessing.Queue`. 

This specialized structure uses underlying pipe architectures, locks, and system threads to ensure thread-safe and process-safe operations. I embedded a **sentinel pattern** (`None` markers) at the tail of the data stream. When a worker pulls a sentinel, it handles the shutdown signal cleanly and exits, preventing worker hangs or zombie processes.

## Complexity Profile
* **Runtime Bounds:** Task pushes and pulls resolve in $O(1)$ constant time.
* **Space Constraints:** Scales at $O(N)$ memory allocations based on the maximum volume of items held in the queue.