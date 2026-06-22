# Logic Breakdown: Longest Increasing Subsequence (LIS)
**Engineer:** Syed Saad Bin Irfan

## The Problem
Identifying sequential trends inside irregular data blocks (such as mapping long-term stock growth peaks or tracking file revision histories) is challenging because the values don't need to sit right next to each other. Isolating the longest continuous rising chain requires comparing each new entry against everything that came before it.

## My Approach
I built a nested state scanning engine. The tracker initializes an array where every position starts with a baseline value of `1`. A pair of nested loops then scans the data: the outer loop steps forward through the sequence, while the inner loop checks all historical values behind it. When the outer value beats a past value, the engine applies the update rule:

$$dp[i] = \max(dp[i], dp[j] + 1)$$

This safely records the longest stepping chain found up to that point.

## Critical Thinking
*   **Time Complexity:** Enforced at a quadratic $O(N^2)$ tier due to its nested historical scans.
*   **Space Complexity:** Requires a straightforward linear $O(N)$ layout to store tracking values.

This structural tracking approach provides an exceptionally clear way to audit trends and run sequence alignments across fluctuating data sets.