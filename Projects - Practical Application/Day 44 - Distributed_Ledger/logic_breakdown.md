# Portfolio Architectural Review: Distributed Financial Ledger System
**Lead Engineer:** Syed Saad Bin Irfan

## Practical Context
In enterprise core banking and microservice-driven payment platforms, transaction accuracy is critical. If a payment process debits a sender's balance but a network failure prevents the receiver from getting credited, data consistency is broken. This system implements a Two-Phase Commit architecture to ensure updates across distributed database instances either succeed completely or roll back cleanly.

## Core Problem Space & Challenges
1. **Partial Execution Failures:** If individual database nodes perform operations in isolation without coordination, a mid-operation crash can leave data half-updated, causing data mismatches.
2. **Volatile Memory Losses:** If a database node crashes and reboots, any uncommitted transaction states stored in its active memory are lost, making it difficult to recover or roll back safely.
3. **Strict Validation Checks:** The system must confirm all resource allocations and account balances are valid *before* any permanent changes are written to disk across the cluster.

## My Technical Solution & Implementation Approach
* **Two-Phase Commit Protocol Execution:** The application splits transactions into two distinct steps controlled by a central coordinator. Phase 1 asks all participant nodes if they can safely accept the write. Only if every node votes yes does Phase 2 issue the final, atomic commit command to save the changes across the cluster.
* **Write-Ahead Logging Mechanics:** Database nodes log their intent to disk before updating any runtime variables. This persistent logging ensures that if a crash occurs mid-transaction, the system can parse the log file to replay completed operations or clean up half-finished updates.
* **Decoupled Architecture Composition:** The code avoids monolithic design traps by splitting responsibilities across 6 clean, dedicated modules (`transaction.py`, `ledger.py`, `participant.py`, `coordinator.py`, `metrics.py`, and `main.py`). This clean decoupling makes components easy to test and maintain, following professional development standards.

## Complexity Profile Analysis
* **Runtime Bounds:**
  * Transaction Phase Coordination: Running consensus verification scales linearly at $O(N)$ time relative to participant node count $N$.
  * Local Balance Verification: Node-level balance lookups and updates execute in fast $O(1)$ constant time.
* **Memory Constraints:** System memory use grows at a steady $O(A + N)$ space boundary to manage active accounts $A$ and track network node configurations $N$.