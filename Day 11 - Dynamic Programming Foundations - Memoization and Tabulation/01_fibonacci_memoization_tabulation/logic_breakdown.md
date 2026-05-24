# Logic Breakdown: Memoization and Tabulation Foundations
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard recursive algorithms recalculate identical sub-states repeatedly, driving execution speeds down to an exponential $O(2^N)$ crawl. We need a clean, structured way to intercept recurring calls, ensuring every unique value variant is evaluated exactly once.

## My Approach
I built two alternative optimization frameworks. The Top-Down Memoization engine uses a dictionary to cache results mid-execution, skipping redundant sub-branches. The Bottom-Up Tabulation engine works in reverse: it initializes an entry array and builds values forward from baseline states, avoiding recursive stack overhead entirely.

## Critical Thinking
*   **Time Complexity:** Both approaches collapse execution times down to a linear $O(N)$ runtime.
*   **Space Complexity:** Both frameworks scale at $O(N)$ memory depth, though Memoization incurs additional call stack overhead.

This foundational contrast helps you select the right DP pattern for your needs, showing how storing state data prevents execution blowouts.