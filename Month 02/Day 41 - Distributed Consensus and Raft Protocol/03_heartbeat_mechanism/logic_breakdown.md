# Logic Breakdown: Authority Maintenance via Empty Heartbeats
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a leader wins an election, it must continuously declare its authority to prevent followers from timing out and starting unnecessary new elections.

## My Approach
I implemented an **Empty AppendEntries RPC Heartbeat Generator**.

Instead of inventing a unique messaging protocol for health checks, Raft repurposes the log replication message. By sending an `AppendEntries` RPC with an empty log array, the leader resets the election timers on all followers without writing new data to their logs.

## Complexity Profile
* **Runtime Bounds:** Packaging the heartbeat message takes $O(1)$ constant time.
* **Space Constraints:** Storage structures require $O(1)$ constant auxiliary allocation memory.