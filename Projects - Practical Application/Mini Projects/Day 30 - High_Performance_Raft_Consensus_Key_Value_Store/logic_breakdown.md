# Portfolio Code Review: Distributed Fault-Tolerant Raft Consensus Key-Value Storage Engine
**Author:** Syed Saad Bin Irfan

## Practical Context
This engine simulates the consensus mechanics used by highly available systems (like etcd or Consul) to maintain consistent system configurations and transactional records across an entire cluster.

## Engineering Standards Applied
* **Decentralized Role Transitions:** Encapsulates role behavior logic (`FOLLOWER`, `CANDIDATE`, `LEADER`) directly inside the node object, removing the need for an external orchestrator during election cycles.
* **Majority Quorum Enforcement:** Enforces strict quorum rules during write paths. Transactions are only committed to the underlying database after confirmation from a mathematical majority ($\lfloor N/2 \rfloor + 1$) of nodes.
* **Monotonic Term Tracks:** Uses incrementing term counters to detect and drop out-of-date messages instantly, ensuring older, delayed network requests cannot disrupt the cluster state.