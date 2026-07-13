# Logic Breakdown: Write-Ahead Saga Log Durability
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If the host server crashes mid-transaction, an in-memory orchestrator loses its place in the workflow. When it reboots, it won't know which microservices already committed changes, leading to orphaned resources or double charges.

## My Approach
I implemented a write-ahead journal simulator. Before handing off a transaction step to an external network service, the orchestrator serializes its current state and flushes it to a durable log history tracker. This gives the system a reliable recovery blueprint to read from when recovering after a crash.

## Complexity Profile
* Runtime Bounds: Appending and reading log history records takes constant time $O(1)$.
* Space Constraints: Memory footprint scales linearly $O(M)$ with the total number of logged state changes.