# Logic Breakdown: Linear String Processing (Z-Algorithm)
**Engineer:** Syed Saad Bin Irfan

## The Problem
String matching algorithms often require managing separate state structures or complex backward steps. We need a clean, uniform approach that solves pattern matching by treating the pattern and text as a single combined string.

## My Approach
I implemented the **Z-Algorithm**. This approach builds a single `Z-array` over a unified string formatted as:

$$\text{Combined} = \text{Pattern} + \text{"\$"} + \text{Text}$$

Each element `Z[i]` tracks the exact length of the longest substring starting at `i` that matches the prefix of the entire string.

The engine optimizes this process by maintaining a sliding window $[L, R]$ that tracks the rightmost prefix match found so far. If a new index falls inside this window, the engine copies its value from a previously computed position. It manually scans and expands characters only when an index extends past the current $R$ boundary, keeping the process fast and linear.

## Complexity Profile
* **Execution Time:** Strictly linear $O(N + M)$ performance.
* **Space Complexity:** $O(N + M)$ memory footprint to store the combined string and array.