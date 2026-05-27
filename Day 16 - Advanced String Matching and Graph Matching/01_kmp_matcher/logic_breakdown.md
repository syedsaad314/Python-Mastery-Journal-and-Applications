# Logic Breakdown: Knuth-Morris-Pratt (KMP) String Matching
**Engineer:** Syed Saad Bin Irfan

## The Problem
A naive string search compares character by character, shifting the pattern forward by exactly one position whenever a mismatch occurs. This causes the text pointer to backtrack constantly, leading to an inefficient worst-case runtime of $O(N \times M)$.

## My Approach
I implemented the **Knuth-Morris-Pratt (KMP)** algorithm. The key optimization is avoiding backtracking by analyzing the pattern itself beforehand.

I built an **LPS (Longest Prefix Suffix) array**. Each index `LPS[i]` tracks the length of the longest proper prefix that is also a suffix for the substring ending at `i`. When a mismatch occurs after a partial match, the engine looks up the LPS array to determine how much of the pattern can be safely skipped, allowing the text pointer to move steadily forward.

## Complexity Profile
* **Precomputation Time:** $O(M)$ to generate the lookup array.
* **Matching Runtime:** Strictly bounded at $O(N)$ linear time.
* **Space Complexity:** $O(M)$ to preserve the tracking states.