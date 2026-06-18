# Logic Breakdown: Term-Based Safety Validations
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a network partition heals, an old leader might rejoin the cluster and attempt to send commands or heartbeats, which could overwrite newer data if left unchecked.

## My Approach
I implemented a **Term-Based Safety Validation Interceptor**.

Raft uses logical terms as a monotonic clock to detect stale nodes. If an incoming message contains a term lower than the node's current term, the message is immediately dropped. This prevents outdated leaders from disrupting an active, healthy cluster.

## Complexity Profile
* **Runtime Bounds:** Evaluates conditions and logic paths in $O(1)$ constant time.
* **Space Constraints:** Operates within $O(1)$ constant execution tracking space.