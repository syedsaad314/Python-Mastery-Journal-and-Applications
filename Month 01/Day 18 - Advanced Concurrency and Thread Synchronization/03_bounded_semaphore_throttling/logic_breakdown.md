# Logic Breakdown: Bounded Semaphore Throttling
**Engineer:** Syed Saad Bin Irfan

## The Problem
While locks restrict access to a single user, some scenarios require allowing a specific number of concurrent connections (like a database pool capped at 10 active slots) while blocking further entries.

## My Approach
I utilized a `BoundedSemaphore` configured to allow a fixed number of concurrent workers. Every time a thread enters the context block, the internal counter decrements. Once the counter hits zero, subsequent threads are blocked until an active thread exits and increments the counter, providing a stable system throttling mechanism.

## Complexity Profile
* **Runtime Bounds:** Throttled concurrent execution groups bounded at $O(\text{Total Threads} / \text{Max Slots})$.
* **Space Constraints:** $O(1)$ constant internal counter space allocation tracking.