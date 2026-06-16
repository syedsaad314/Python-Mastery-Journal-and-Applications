# Logic Breakdown: Forward Recovery Retry Mechanics
**Engineer:** Syed Saad Bin Irfan

## The Problem
Not all distributed system errors require an immediate, expensive transaction rollback. Many failures are transient network drops or temporary timeouts that resolve themselves within a few milliseconds.

## My Approach
I implemented a **Forward Recovery Retry Engine with Exponential Backoff**.

Instead of triggering an immediate rollback on a network failure, the orchestrator intercepting the error retries the step using a smart backoff strategy. It scales the delay between attempts exponentially (e.g., 100ms, 200ms, 400ms) to give the downstream service time to recover, safely continuing the transaction without wasting resources on unnecessary rollbacks.

## Complexity Profile
* **Runtime Bounds:** Runs in $O(A)$ time relative to the maximum number of allowed execution retry attempts $A$.
* **Space Constraints:** Operates within $O(1)$ constant execution memory tracking space.