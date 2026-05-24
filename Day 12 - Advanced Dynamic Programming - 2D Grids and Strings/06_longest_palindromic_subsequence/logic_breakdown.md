# Logic Breakdown: Longest Palindromic Subsequence (LPS)
**Engineer:** Syed Saad Bin Irfan

## The Problem
Isolating symmetric sequence patterns within raw data strings is a core challenge in text validation, parsing engines, and computational biology. A subsequence doesn't require characters to sit strictly adjacent to one another, which means standard two-pointer tracking models break down when encountering mismatched gaps.

## My Approach
I built a 2D interval tabulation engine. Instead of reversing the string and running a separate Longest Common Subsequence (LCS) scan, this implementation scores intervals natively. 

Every individual character is initialized as a valid palindrome of length 1. The engine then expands an evaluation window across the text block:
* **If boundary characters match (`seq[i] == seq[j]`):** The inner core value is pulled forward and extended by 2.
* **If boundary characters conflict (`seq[i] != seq[j]`):** The engine cross-checks adjacent sub-intervals and carries forward the dominant maximum value.

$$dp[i][j] = \max(dp[i+1][j], dp[i][j-1])$$

This ensures we catch the longest symmetric sequence without scanning unnecessary character combinations.

## Critical Thinking
* **Time Complexity:** $O(N^2)$ to systematically evaluate all index interval pairs.
* **Space Complexity:** Bounded at $O(N^2)$ to preserve the subproblem tracking matrix.

This clean interval strategy handles structural string variations gracefully, providing a robust layout for pattern matching and text analytics.