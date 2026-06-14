# Logic Breakdown: Raft Pre-Vote Safety Phase
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a node is isolated in a minority partition, its election timer will repeatedly expire, forcing it to increment its term count and start futile elections. When the partition heals, this node will rejoin with a massive term number, forcing the valid cluster leader to step down and disrupting the entire system.

## My Approach
I implemented a **Raft Pre-Vote Safety Protocol Guard**.

Before incrementing its term and starting a real election, a node enters a speculative `Pre-Vote` phase. It polls reachable peers to see if its log is up-to-date and if a cluster majority is reachable. If it cannot see a quorum majority, it stays in the follower state and leaves its term count unchanged, protecting the healthy majority from unnecessary disruptions.

## Complexity Profile
* **Runtime Bounds:** Pre-vote evaluation completes in $O(P)$ time, where $P$ is the number of reachable peers.
* **Space Constraints:** Operates within $O(1)$ constant tracking space.