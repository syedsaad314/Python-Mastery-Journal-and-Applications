# Decentralized Gossip Membership Engine

## Operational Architecture & Topology Invariants
* **Peer-to-Peer State Spread**: Uses randomized peer interaction blocks to discover membership changes without a central registry.
* **Infection-Based Merges**: Evaluates incoming data sets against local views, updating internal registries only when incoming heartbeat counters are strictly higher.
* **Causal Failure Tracking**: Monitors logical counter intervals instead of server clocks, flagging stagnant nodes as `DEAD` across the cluster automatically.

## Code Blueprint
* `models.py`: Declares formats for metadata entries and gossip messages.
* `gossip_node.py`: Implements table mutation logic, anti-entropy loops, and liveness checks.
* `network_simulator.py`: Manages network packet routing and mock node disconnections.