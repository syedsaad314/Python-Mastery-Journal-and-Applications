# Logic Breakdown: Hash Ring Initialization
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard modulo hashing ($hash(key) \pmod N$) causes data loss when cluster size changes, as almost every key maps to a completely different node.

## My Approach
I built a sorted list structure representing a continuous logical hash ring spanning $0$ to $2^{32}-1$. Nodes are assigned positions on this ring by hashing their unique identifiers.

## Complexity Profile
* Runtime Bounds: Insertion costs $O(N \log N)$ due to sorting. Lookups take $O(\log N)$ via binary search.
* Space Constraints: Scaled linearly at $O(N)$ matching physical node counts.