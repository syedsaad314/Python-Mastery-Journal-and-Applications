# Logic Breakdown: Saga Orchestrator State Tracking
**Engineer:** Syed Saad Bin Irfan

## The Problem
When dealing with distributed tasks across distinct, disconnected data engines, we cannot use a single database transaction. If step 3 fails, the system must know exactly how far it progressed forward so it can execute the appropriate corrective actions backward.

## My Approach
I implemented a centralized **Saga Orchestrator State Machine**.

The orchestrator explicitly tracks workflow milestones sequentially. Rather than locking databases, it breaks a distributed transaction into a series of local database transactions. The FSM manages step execution and handles transitions cleanly: if a step succeeds, it advances; if a step fails, it changes the workflow status to `COMPENSATING` to initiate backward cleanup.

## Complexity Profile
* **Runtime Bounds:** Advancing states and validating transitions runs in $O(1)$ constant time.
* **Space Constraints:** Requires $O(1)$ constant memory overhead to track status variables.