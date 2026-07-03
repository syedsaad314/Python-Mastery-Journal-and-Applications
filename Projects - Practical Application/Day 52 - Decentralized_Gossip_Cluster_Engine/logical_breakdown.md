# Engineering Log Overview: Decentralized Gossip Cluster Engine
**Lead Engineer:** Syed Saad Bin Irfan

## 1. The Core Problem
In standard centralized architectures, a master node tracks cluster membership. If that master node crashes, the entire cluster breaks. To build a highly resilient architecture, we need a decentralized way for nodes to self-discover and monitor cluster health without relying on a single point of failure.

## 2. Architectural Brainstorming & Trade-offs
We designed an asymmetric peer-to-peer membership framework using randomized gossip.

### The Trade-offs of Eventual Consistency
* **The Drawback:** Gossip takes time to travel across the network. Changes don't update instantly, meaning some nodes will temporarily hold older views of the cluster state.
* **The Benefit:** The system scales smoothly to thousands of servers. There is no single point of failure, and the network handles brief disconnects without dropping data.
* **Anti-Entropy Optimization:** To resolve network lag, we added an active anti-entropy background step. This runs full table syncs between nodes to quickly bring out-of-date registries up to speed.

## 3. Engineering Implementation Details
* **Infection Engine Execution:** Every node periodically steps its heartbeat counter and passes its entire membership map to a randomly selected peer. This spreads status updates through the network like a virus.
* **Liveness Gaps:** Rather than using physical clocks, nodes use logical counter comparisons. If a peer's counter falls significantly behind the local node's timeline, it is flagged as `DEAD`.