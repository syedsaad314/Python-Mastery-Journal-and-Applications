# Logic Breakdown: Lowest Common Ancestor (LCA) via Binary Lifting
**Engineer:** Syed Saad Bin Irfan

## The Problem
Finding the **Lowest Common Ancestor (LCA)** of two nodes in a massive organizational chart or tree network by scanning upward step-by-step takes an inefficient $O(H)$ linear time, where $H$ is tree height. To scale efficiently, we need a way to hop upward through the tree hierarchy in logarithmic time.

## My Approach
I implemented an LCA engine using **Binary Lifting**. This optimization maps out parent jump connections across a structured table layout (`up[node][j]`), allowing nodes to jump upward by powers of two ($2^j$).

Node (Depth 8) 
      |  \
      |   Jump 2^2 (4 steps up) -> Ancestor (Depth 4)
      v
   Jump 2^0 (1 step up) -> Parent (Depth 7)

1. **Precomputation:** A single DFS pass maps node depths and populates the immediate parents at power $2^0$. It then calculates higher-level jumps using the property that jumping $2^j$ steps upward is equivalent to taking two successive jumps of size $2^{j-1}$:
   $$\text{up}[node][j] = \text{up}[\text{up}[node][j-1]][j-1]$$
2. **Depth Alignment:** When querying nodes $U$ and $V$, the deeper node is lifted upward using bitwise shifts until both nodes share the same depth layer.
3. **Simultaneous Binary Search:** Both nodes jump upward together using decreasing powers of two. They skip matching ancestor paths until they land exactly one level beneath their lowest common ancestor.

## Performance Profile
* **Precomputation Cost:** $O(N \log N)$ during initialization.
* **Query Match Speed:** Bounded at $O(\log N)$ jump steps.
* **Memory Footprint:** $O(N \log N)$ to maintain the binary lifting matrix.

This optimization technique is key for resolving inheritance chains in object compilers, calculating network routing path intersections, and managing database dependency lines.   