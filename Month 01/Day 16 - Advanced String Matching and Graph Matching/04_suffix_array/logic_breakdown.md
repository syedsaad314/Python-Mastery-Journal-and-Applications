# Logic Breakdown: Suffix Array & LCP Indexing
**Engineer:** Syed Saad Bin Irfan

## The Problem
To perform advanced text analysis—such as finding the longest repeating substring or counting pattern occurrences—re-scanning the string repeatedly is highly inefficient. We need a way to pre-sort and index all substrings to enable fast, optimized lookups.

## My Approach
I implemented a **Suffix Array** structure combined with an **LCP (Longest Common Prefix) array**.

1. **Suffix Sorting:** Instead of sorting all suffix variations independently (which would take $O(N^2 \log N)$ time), the engine uses a **Prefix Doubling** technique. It sorts chunks of length $K$, then combines their relative ranks to sort chunks of length $2K$, accelerating the process.
2. **LCP Generation:** Using **Kasai's Algorithm**, the engine builds the LCP array in linear time. It leverages the property that the prefix match length drops by at most 1 when stepping from suffix $i$ to suffix $i+1$, avoiding redundant character comparisons.

## Complexity Assessment
* **Suffix Array Generation:** $O(N \log^2 N)$ using standard sorting operations.
* **LCP Array Generation:** Efficient linear $O(N)$ execution.
* **Applications:** Enables binary search pattern matching in $O(M \log N)$ time.