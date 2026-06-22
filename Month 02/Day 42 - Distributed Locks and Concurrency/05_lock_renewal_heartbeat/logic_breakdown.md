# Logic Breakdown: Lock Renewal Heartbeats
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Setting a short Lease TTL protects the system against node crashes, but introduces a new risk: a complex, healthy job might take longer than expected, causing its lease to expire prematurely and letting other nodes claim the resource mid-execution.

## My Approach
I built a **Lock Renewal Heartbeat Agent**.

The design keeps the initial Lease TTL short to ensure quick recovery if a crash occurs. To prevent active tasks from losing their locks, a background process monitors the job and automatically extends the lease window (renewing the TTL) as long as the worker thread confirms it is still running healthily.

## Complexity Profile
* **Runtime Bounds:** Evaluation and lease update modifications run in $O(1)$ constant time.
* **Space Constraints:** Allocation bounds scale at $O(1)$ constant storage tracking space.