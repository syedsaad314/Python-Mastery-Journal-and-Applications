# Logic Breakdown: Knuth-Morris-Pratt (KMP) Linear Matcher
**Engineer:** Syed Saad Bin Irfan

## The Problem
Brute-force string matching uses nested loops to check for a pattern. When a character mismatch occurs midway through an evaluation, the pointer resets back to the start of the match attempt. This backward jumping causes an inefficient $O(N \times M)$ runtime.

## My Approach
I implemented the **Knuth-Morris-Pratt (KMP)** algorithm, which achieves a true linear runtime. 

It works by pre-processing the pattern to generate a **Longest Prefix Suffix (LPS)** array. This table tracks where the pattern contains repeating structural segments. 

When a mismatch occurs against the main body of text, the engine references the LPS table to determine the next alignment position. This allows the pointer to move continuously forward through the text stream without ever back-tracking.

## Architectural Metrics
* **Time Complexity:** Pre-computation takes $O(M)$ time, and the core text search runs in $O(N)$ time. This yields a stable **$O(N + M)$** total runtime.
* **Space Complexity:** Bounded efficiently at $O(M)$ to store the tracking integers inside the LPS table.