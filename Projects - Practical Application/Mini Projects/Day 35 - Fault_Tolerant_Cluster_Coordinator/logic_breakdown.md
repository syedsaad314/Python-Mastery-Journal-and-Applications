# Portfolio Code Review: Fault-Tolerant Cluster Coordinator
**Author:** Syed Saad Bin Irfan

## Practical Context
This simulator models how distributed systems like Kubernetes (via Etcd) or distributed data planes handle server failures on the fly, demonstrating how clusters automatically maintain availability using quorum consensus.

## Engineering Standards Applied
* **Graceful Failure Rebalancing:** Simulates real-world leader crashes, showing how candidate nodes automatically step up to trigger elections when heartbeats stop.
* **Strict Quorum Recovery Checks:** Enforces strict majority checks during recovery elections, ensuring a replacement leader can only take over if it secures enough active votes.
* **Dead-Node Isolation Safety:** Ignores crashed or unreachable nodes during elections, preventing offline servers from locking up or breaking cluster consensus.