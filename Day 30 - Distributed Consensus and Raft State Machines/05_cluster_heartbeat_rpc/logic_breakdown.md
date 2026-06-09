# Logic Breakdown: Cluster Heartbeat RPC Coordinator
**Engineer:** Syed Saad Bin Irfan

## The Problem
Once an election completes, the leader must continuously assert its authority across the cluster. Without routine updates, follower nodes will assume the leader has failed and trigger new elections, causing disruptive cluster churn.

## My Approach
I implemented a simplified **Heartbeat Broadcast Coordination** layer.

The leader node runs a routine loop that sends empty `AppendEntries` RPC packets to all registered peer addresses at regular intervals (e.g., every 50ms). When followers process these empty updates, they treat them as a keep-alive signal and reset their local election timers, keeping the cluster stable and unified under the current term leader.

## Complexity Profile
* **Runtime Bounds:** Broadcasting updates scales linearly ($O(N)$) based on the number of peers in the cluster.
* **Space Constraints:** Uses minimal $O(N)$ memory allocations to track lease expiration records for each peer node.