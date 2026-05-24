# Logic Breakdown: 0/1 Knapsack Grid Optimization
**Engineer:** Syed Saad Bin Irfan

## The Problem
When allocating server resources or loading cargo, you have limited capacity. A greedy approach (picking the most valuable item first) fails because taking a high-value, massive item might block you from taking several smaller items that together hold greater value. We need to evaluate every possible sub-capacity.

## My Approach
I utilized a **2D Matrix Tabulation** engine. The rows represent the available items, and the columns represent incremental weight capacities from $0$ up to the limit. At each cell, the engine makes a binary choice: *Exclude* the item (carry forward the best value from the row above) or *Include* it (add its value to the optimal state of the remaining capacity). The matrix guarantees the absolute highest yield at the bottom-right corner.

## Critical Thinking
*   **Time Complexity:** Operates at $O(N \times W)$, where $N$ is items and $W$ is the max capacity. 
*   **Space Complexity:** Matches at $O(N \times W)$ to hold the tracking grid.

This establishes the baseline constraint logic required for advanced resource allocation algorithms in backend scheduling systems.