# Distributed Linearizable Read Subsystem

## Architectural Proof & Consistency Invariants
* **Linearizable Consistency Guarantees**: Prevents stale reads by establishing strict `ReadIndex` baseline limits or utilizing time-bounded leader leases.
* **Clock Drift Safety Thresholds**: Automatically shrinks lease windows using conservative safety buffer calculations ($Drift_{max}$) to protect against CPU wall-clock drift across physical servers.
* **Strict Mutation Idempotency**: Deduplicates retried client operations using structural session history vaults to ensure that a mutation is executed exactly once, even if network requests time out or fail.

## Component Map
* `models.py`: Structural definitions for data requests, queries, and lease packets.
* `lease_manager.py`: Controls lease tracking, time evaluations, and drift safety.
* `read_index_engine.py`: Captures monotonic commit metrics and evaluates quorum acknowledgments.
* `session_store.py`: Caches client transaction states to prevent duplicate mutation execution.
* `kv_replica.py`: Serves as the local key-value state store.
* `orchestrator.py`: Implements branching logic to direct traffic to the optimal linearizable read or write path.