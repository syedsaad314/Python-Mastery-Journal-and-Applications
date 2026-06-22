# Logic Breakdown: Mo's Algorithm (Offline Range Queries)
**Engineer:** Syed Saad Bin Irfan

## The Problem
When processing a large collection of range queries on an array, evaluating each one independently can result in significant redundant scanning, leading to an inefficient $O(Q \times N)$ runtime. If the dataset is static, we need a way to reorganize these requests to minimize pointer movement and optimize performance.

## My Approach
I implemented **Mo's Algorithm**, an offline optimization technique that groups queries by partitioning the array into blocks of size $\sqrt{N}$. 

Queries are sorted using two conditions:
1. **Primary Sort:** Grouped by the square-root block index of their left boundary ($\lfloor L / \sqrt{N} \rfloor$).
2. **Secondary Sort:** Sorted in ascending order by their right boundary ($R$).

Block 0 (Size sqrt(N))   Block 1 (Size sqrt(N))   Block 2 (Size sqrt(N))
[ Q1_L,       Q1_R ]   [ Q2_L,                Q2_R ]

Sorting the queries this way ensures that as the engine steps through them, the left and right pointers slide smoothly across the array rather than jumping erratically. This minimizing of index adjustments significantly speeds up processing across the entire batch of requests.

## Complexity Assessment
* **Query Reordering Cost:** $O(Q \log Q)$ sorting step.
* **Pointer Movement Total:** Strictly bounded at **$O((N + Q) \sqrt{N})$** operations.
* **Space Constraints:** Requires $O(Q)$ memory to preserve and map answers.

This offline strategy is highly effective for heavy data analytics, batch log processing, and historical database reporting tools.