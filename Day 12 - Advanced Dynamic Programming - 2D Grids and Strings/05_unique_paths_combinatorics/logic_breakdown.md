# Logic Breakdown: Unique Path Combinations
**Engineer:** Syed Saad Bin Irfan

## The Problem
Instead of finding the *cheapest* path, we sometimes need to quantify the *total number* of possible paths to calculate probability, traffic load dispersion, or network redundancy across a set matrix. 

## My Approach
This is pure dynamic combinatorics. I start by laying down a grid of `1`s. The reasoning is structural: if you are locked to the top row, there is exactly $1$ way to get anywhere (keep moving right). For every internal cell, the total number of ways to reach it is simply the sum of the paths leading into it from above and from the left. 

$$dp[i][j] = dp[i-1][j] + dp[i][j-1]$$

This perfectly mirrors Pascal's Triangle mapped onto a rectangular matrix format.

## Critical Thinking
*   **Time Complexity:** Linear scan of the grid boundaries at $O(R \times C)$.
*   **Space Complexity:** $O(R \times C)$ for the accumulation table.

A lightweight, flawless way to calculate structural network redundancy limits without relying on heavy factorial math.