# Logic Breakdown: Async Synchronization Primitives
**Engineer:** Syed Saad Bin Irfan

## The Problem
Even though async code runs inside a single thread, concurrent access can still cause logical race conditions or trigger API rate limit bans if too many requests hit a remote endpoint simultaneously.

## My Approach
I implemented an `asyncio.Semaphore` to manage connection limits. 

Unlike multi-threaded locks that block an entire execution thread, the async semaphore simply pauses the calling coroutine and parks it until a slot opens up. The event loop continues running other active tasks, maintaining high performance while strictly enforcing downstream connection limits.

## Complexity Profile
* **Runtime Bounds:** $O(1)$ constant lookup overhead.
* **Space Constraints:** Constant $O(1)$ internal primitive tracking state footprint.