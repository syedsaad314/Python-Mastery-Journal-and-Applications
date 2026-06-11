# Portfolio Code Review: Peer-to-Peer Anti-Entropy Sync Engine
**Author:** Syed Saad Bin Irfan

## Practical Context
This synchronization framework mirrors the background anti-entropy mechanisms used by distributed datastores to fix data drift caused by missed writes or server crashes without putting high stress on network connections.

## Engineering Standards Applied
* **Logarithmic Data Drift Isolate:** Traverses trees side-by-side to find out-of-sync ranges in $O(\log K)$ logarithmic time, avoiding heavy full-table scans.
* **Bandwidth Optimization Structural Blueprint:** Compares tree structures by swapping root hashes first, keeping network usage low when datasets are mostly identical.
* **Decentralized Pairwise Merging Engine:** Allows replicas to sync directly with any peer in the cluster, avoiding central choke points and ensuring reliable, distributed consistency.