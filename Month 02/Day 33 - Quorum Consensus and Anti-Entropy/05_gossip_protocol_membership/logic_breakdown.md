# Logic Breakdown: Gossip Protocol Failure Detection
**Engineer:** Syed Saad Bin Irfan

## The Problem
In fully decentralized architectures without a central coordinator, nodes need a reliable way to monitor cluster health, track additions, and detect server crashes without overloading the network with central polling.

## My Approach
I built a **Decentralized Gossip Protocol Simulator**.

Each node maintains an internal vector tracking versioned heartbeat counters for every known server in the cluster. Periodically, each node increments its own counter and shares its entire health matrix with a randomly selected peer. As nodes constantly exchange metadata, health states and node updates spread quickly through the cluster (scaling exponentially), ensuring all nodes reach agreement on cluster status without needing a single coordinator.

## Complexity Profile
* **Runtime Bounds:** Processing and merging incoming metadata states takes $O(N)$ linear time relative to cluster size.
* **Space Constraints:** Requires $O(N)$ memory per node to store the tracking states for all cluster members.