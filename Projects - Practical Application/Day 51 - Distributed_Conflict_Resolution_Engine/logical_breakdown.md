# Engineering Log Overview: Distributed Conflict Resolution Engine
**Lead Engineer:** Syed Saad Bin Irfan

## 1. The Core Problem
In decentralized architectures, system nodes accept writes independently to maintain high availability. During network partitions, different nodes might update the exact same database key at the same time. Since physical server clocks suffer from clock drift, relying on standard timestamps to order these writes can cause data loss, dropping valid updates silently.

## 2. Architectural Brainstorming & Trade-offs
To solve this problem without a central authority, we replaced physical clock timestamps with logical **Vector Clocks**.

### Choosing the Multi-Version Storage Pattern (Siblings)
* **The Trade-off:** Instead of forcing a "Last-Write-Wins" policy that risks losing data, we built a multi-version data storage vault.
* **The Mechanics:** When an incoming update is flagged as concurrent, the engine splits the storage layer into multiple parallel "sibling" versions. This guarantees no data is dropped during a network split, leaving conflicts visible so they can be merged cleanly once the partition heals.

## 3. Engineering Implementation Details
* **Causal Ordering Logic:** Vector entries are cross-referenced across nodes. If Vector A has greater values than Vector B in some positions but lower values in others, the engine flags a concurrency conflict.
* **Reconciliation via Merges:** When merging sibling records, the engine calculates the element-wise maximum across all active clocks. This unifies their histories and creates a clean baseline for future updates.