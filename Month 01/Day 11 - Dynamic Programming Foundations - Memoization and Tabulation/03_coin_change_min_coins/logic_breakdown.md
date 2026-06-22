# Logic Breakdown: Unbounded Optimization Tables
**Engineer:** Syed Saad Bin Irfan

## The Problem
Simple greedy strategies often struggle with mixed currency pools or custom allocation sets because picking the largest option first can lead to dead ends or sub-optimal combinations. To guarantee you find the absolute fewest elements needed to hit a target sum, you have to systematically evaluate and score every potential sub-combination path.

## My Approach
I implemented an iterative optimization matrix. The engine initializes an array of size $Target + 1$ filled with infinity values, setting the base case index `0` to zero. It loops through every amount from 1 up to the target, testing every coin choice. The state transition updates the current slot using the minimization rule:

$$dp[i] = \min(dp[i], dp[i - \text{coin}] + 1)$$

This guarantees that each slot captures the absolute lowest coin requirement possible.

## Critical Thinking
*   **Time Complexity:** Scales efficiently at $O(\text{Target} \times N)$, where $N$ represents the size of the elements pool.
*   **Space Complexity:** Bounded cleanly to a single array allocation of $O(\text{Target})$.

This structured matrix search handles erratic element denominations effortlessly, making it a reliable fit for logistics distribution setups and financial clearing systems.