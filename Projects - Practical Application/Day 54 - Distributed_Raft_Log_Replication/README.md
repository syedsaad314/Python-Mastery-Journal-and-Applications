# Distributed Raft Log Replication Engine

## Fundamental Data Guarantees
* **Log Matching Safety Invariant**: Enforces that if two independent node server instances contain matching entries at the same index and term, their entire log history matches up to that point.
* **Deterministic Execution Flow**: Ensures that commands are only fed into the storage engine after achieving a verified quorum majority, completely shielding your application state from uncommitted election churn.
* **Automated Log Alignment**: Automatically rolls back and overwrites conflicting, uncommitted follower entries to keep the cluster perfectly synchronized with the active leader.

## Component Layout
* `models.py`: Holds immutable structural definitions for log payloads and message envelopes.
* `state_machine.py`: Drives internal database mutations via an encapsulated key-value engine.
* `network_stub.py`: Routes synchronous update packets between cluster members.
* `raft_node.py`: Manages validation logic, replication loops, and pointer backtracking.