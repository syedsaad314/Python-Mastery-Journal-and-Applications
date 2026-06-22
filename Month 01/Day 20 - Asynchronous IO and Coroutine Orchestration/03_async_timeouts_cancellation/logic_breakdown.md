# Logic Breakdown: Defensive Async Timeouts and Task Cancellations
**Engineer:** Syed Saad Bin Irfan

## The Problem
Unresponsive remote servers can stall async workers indefinitely, draining memory and leaking open connection sockets across the application pool.

## My Approach
I used `asyncio.wait_for()` to enforce a hard timeout ceiling on operations. 

When the timeout expires, the runtime throws an `asyncio.TimeoutError` and automatically injects an `asyncio.CancelledError` directly into the hanging coroutine. This triggers structured resource rollbacks inside the coroutine's `try/except/finally` block, ensuring clean socket closures and database rollbacks.

## Complexity Profile
* **Runtime Bounds:** Constant $O(1)$ timeout monitoring overhead.
* **Space Constraints:** Flat $O(1)$ tracking allocation profile.