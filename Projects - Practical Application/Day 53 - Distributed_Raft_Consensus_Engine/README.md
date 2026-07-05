# Distributed Raft Consensus Engine

## Core Guarantees & Distributed Invariants
* **Single Leader Invariant**: Guarantees that at most one leader can be elected per term by enforcing absolute cluster majorities ($\lfloor N/2 \rfloor + 1$).
* **Term-Based Chronological Clocking**: Uses monotonic terms to detect and evict outdated leaders instantly when a higher term is observed.
* **Timeout Jitter Optimization**: Implements randomized election windows to prevent concurrent node campaigns from hitting split-vote deadlocks.

## Architectural Blueprint
* `models.py`: Declares structures for vote request/response payloads and heartbeats.
* `network_stub.py`: Manages network broadcast message routing between node instances.
* `raft_node.py`: Implements the core state transition engine and vote validation logic.