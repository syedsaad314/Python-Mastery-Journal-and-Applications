# Logic Breakdown: Random Gossip Target Selection
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If nodes pass states sequentially or communicate along a static tree path, any single node failure can halt information flow across the rest of the cluster.

## My Approach
I utilized a randomized selection model. By picking target nodes at random intervals, information spreads naturally through the network like an infection, giving the architecture exceptional fault tolerance.

## Complexity Profile
* Runtime Bounds: $O(N)$ to scan and filter the membership table.
* Space Constraints: Allocates an $O(N)$ lookup array for filtering out the local node ID.