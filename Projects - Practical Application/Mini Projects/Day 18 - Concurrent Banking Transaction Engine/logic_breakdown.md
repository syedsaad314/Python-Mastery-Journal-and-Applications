# Portfolio Code Review: Concurrent Banking Transaction Engine
**Engineer:** Syed Saad Bin Irfan

## The Problem
In financial ledgers, updates must be atomic to ensure funds are never created or lost during concurrent transfers. Additionally, simple locking structures can introduce serious deadlocks if separate execution threads acquire account resources in opposing orders simultaneously.

## Engineering Standards Applied
* **Deterministic Resource Ordering:** To eliminate deadlock risks completely, the execution pipeline dynamically compares account strings lexicographically before acquiring locks. By ensuring every thread locks accounts in the exact same relational sequence (e.g., lower ID first), we prevent cyclical resource-wait conditions.
* **Atomic State Double-Entry Controls:** Balance checks are deferred until both individual account locks are secured. This prevents race conditions like double-spending, ensuring accurate balance evaluations.
* **Thread-Safe Audit Ledger:** Implements an isolated logging system protected by a dedicated mutex, capturing consistent historical records across all concurrent transaction paths.