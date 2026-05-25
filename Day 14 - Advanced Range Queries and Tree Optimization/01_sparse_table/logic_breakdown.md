# Logic Breakdown: Sparse Table (Static Range Minimum Query)
**Engineer:** Syed Saad Bin Irfan

## The Problem
When calculating values over custom ranges (like finding the minimum element between indices $L$ and $R$), scanning the array directly takes $O(N)$ time per query. If the data is fixed and you need to process thousands of queries, these linear scans create a massive runtime bottleneck.

## My Approach
I implemented a **Sparse Table** structure. It precomputes the answers for all array intervals whose lengths are exact powers of two ($1, 2, 4, 8, \dots$). 

Using a bottom-up table matching pattern, the range value for power $J$ is derived directly from two sub-components calculated during power $J-1$:

$$\text{table}[i][j] = \min(\text{table}[i][j-1], \text{table}[i + 2^{j-1}][j-1])$$

When a query arrives for an arbitrary range $[L, R]$, we calculate the largest power of two ($2^K$) that fits inside the window. Because operations like finding the minimum allow for overlapping regions without changing the result (idempotency), we can overlay two ranges of size $2^K$—one starting at $L$ and the other ending at $R$—to find the correct answer in a single operation.

## Complexity Analysis
* **Precomputation Time:** $O(N \log N)$ to fill the multi-power matrix rows.
* **Query Time:** $O(1)$ constant time lookup.
* **Space Complexity:** $O(N \log N)$ memory allocations for the lookup structures.

This design is optimal for immutable telemetry data systems, historical price trackers, and unchanging analytical datasets.