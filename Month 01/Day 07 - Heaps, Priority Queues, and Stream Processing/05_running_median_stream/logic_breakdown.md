# Logic Breakdown: Live Running Median Stream Partitioning
**Engineer:** Syed Saad Bin Irfan

## The Problem
Calculating the median value of an ongoing data stream (like tracking live server response times) is a notorious bottleneck. Unlike a simple average, the true median depends on position. If you use a standard array, recalculating the median requires sorting it every time a new number arrives, which slows down the system to a crawl at $O(N^2)$ time.

## My Approach
I implemented an optimized two-heap design pattern. A **Max-Heap** holds the smaller half of our dataset, while a **Min-Heap** stores the larger half. As new numbers pour in, they are routed to the appropriate side. The system then automatically balances the heaps so their sizes never differ by more than one element, positioning the exact median values right at the top roots of the tree.

## Critical Thinking
*   **Time Complexity:** Ingesting new elements runs in predictable $O(\log N)$ time, while fetching the live median executes instantly in $O(1)$ time.
*   **Space Complexity:** Scales at $O(N)$, storing stream items uniformly across both heap structures.

This split-pool balancing technique lets you monitor real-time SLA thresholds and system latency changes without processing lags.