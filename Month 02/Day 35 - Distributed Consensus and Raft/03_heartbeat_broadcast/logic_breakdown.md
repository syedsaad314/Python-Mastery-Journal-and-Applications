# Logic Breakdown: Leader Heartbeat Broadcast Routing
**Engineer:** Syed Saad Bin Irfan

## The Problem
Once a leader is elected, it must continuously signal its presence to the cluster. If it fails to send heartbeats, followers will assume it has crashed, start a new election, and disrupt the cluster unnecessarily.

## My Approach
I modeled a **Leader Heartbeat Broadcast Layer**.

The active leader periodically sends empty `AppendEntries` messages to all known peers. When followers receive this message, they reset their election timeout countdowns. This mechanism allows the leader to assert its authority and maintain cluster stability as long as it remains healthy.

## Complexity Profile
* **Runtime Bounds:** Broadcasting messages scales linearly at $O(N)$ based on the number of follower nodes $N$.
* **Space Constraints:** Operates within $O(1)$ auxiliary storage bounds.