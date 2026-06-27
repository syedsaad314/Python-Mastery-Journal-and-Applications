# Logic Breakdown: Virtual Node Distribution
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Mapping only physical nodes to the ring can cause an uneven distribution of data, leaving some servers overloaded while others sit idle.

## My Approach
I interleaved multiple virtual endpoints (VNodes) across the ring for each physical machine. This creates balanced coverage across the entire 32-bit token space.

## Complexity Profile
* Runtime Bounds: Initialization runs at $O(V \log V)$ where $V = N \times \text{vnodes}$.
* Space Constraints: Storage expands linearly with total VNodes ($O(V)$).