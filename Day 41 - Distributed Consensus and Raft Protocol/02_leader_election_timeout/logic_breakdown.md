# Logic Breakdown: Randomized Election Timeouts
**Engineer:** Syed Saad Bin Irfan

## The Problem
If all cluster nodes utilize identical timeouts, they will detect a leader's failure at the exact same moment. They will all transition to Candidates simultaneously, vote for themselves, and trap the system in an infinite loop of split votes.

## My Approach
I built a **Randomized Election Timer Engine**.

By randomizing the election timeout window (typically between 150ms and 300ms), the system guarantees that one node will time out before its peers. This single node will quickly advance its term, declare candidacy, and collect majority votes before other nodes can split the ballot.

## Complexity Profile
* **Runtime Bounds:** Randomization and time evaluation checks occur in $O(1)$ constant time.
* **Space Constraints:** Operates strictly within $O(1)$ constant tracking space.