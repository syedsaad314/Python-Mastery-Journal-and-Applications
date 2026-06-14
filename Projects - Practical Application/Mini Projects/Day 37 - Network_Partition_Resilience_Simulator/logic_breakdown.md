# Portfolio Code Review: Asymmetric Network Partition Resilience Simulator
**Author:** Syed Saad Bin Irfan

## Practical Context
This simulator models how distributed systems like Kubernetes clusters or consensus data planes handle network splits, demonstrating how the Pre-Vote protocol protects the system from split-brain scenarios and disruptive terms.

## Engineering Standards Applied
* **Speculative Election Guard Rails:** Implements a strict Pre-Vote phase that forces candidate nodes to check if a cluster majority is reachable before starting a real election.
* **Disruption Mitigation Safety:** Prevents isolated minority nodes from repeatedly incrementing their term numbers, ensuring they can rejoin the cluster smoothly when the partition heals.
* **Network Topology Abstraction:** Uses an isolated reachability matrix to simulate real-world asymmetric network cuts, allowing us to safely test cluster behavior during partial network failures.