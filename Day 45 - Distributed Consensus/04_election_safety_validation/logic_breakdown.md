# Logic Breakdown: Raft Election Safety Restrictions
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a node with an incomplete log is elected leader, it could overwrite valid, committed logs on other nodes, leading to data loss across the cluster.

## My Approach
I designed a **Raft Election Safety restriction**.
Followers enforce strict rules before voting for a candidate. A follower will deny its vote if the candidate's log is less up-to-date than its own. The candidate's log is considered up-to-date if its last entry has a higher term, or if the terms match but its log is longer ($Index_{candidate} \geq Index_{voter}$). This guarantees the elected leader contains all committed entries from prior terms.

## Complexity Profile
* **Runtime Bounds:** Log status boundary checks execute in $O(1)$ constant time.
* **Space Constraints:** Operates safely within an $O(1)$ constant memory overhead footprint.