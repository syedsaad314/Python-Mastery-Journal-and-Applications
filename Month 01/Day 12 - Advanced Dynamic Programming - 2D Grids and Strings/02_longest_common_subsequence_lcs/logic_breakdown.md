# Logic Breakdown: Longest Common Subsequence
**Engineer:** Syed Saad Bin Irfan

## The Problem
When building diff tools (like Git's internal comparison engine) or DNA sequencing software, you need to find the core overlap between two strings. The characters don't need to be strictly contiguous, but their order must be preserved. A simple linear scan breaks when letters are staggered.

## My Approach
I built a 2D string matrix. `text1` drives the rows and `text2` drives the columns. When the engine encounters a matching character, it looks diagonally backward to the `[row-1][col-1]` cell and adds $1$, effectively linking the new match to the historical chain. If the characters do not match, it pulls the highest historical score from either directly above or directly to the left, ensuring previous matches are never forgotten.

## Critical Thinking
*   **Time Complexity:** Strict $O(M \times N)$ execution based on the lengths of both strings.
*   **Space Complexity:** $O(M \times N)$ memory footprint for the comparison matrix.

This is the exact foundational logic underlying Git conflict resolution and plagiarism detection algorithms.