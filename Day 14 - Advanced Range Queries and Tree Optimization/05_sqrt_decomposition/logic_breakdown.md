# Logic Breakdown: Square Root (Sqrt) Decomposition
**Engineer:** Syed Saad Bin Irfan

## The Problem
Complex tree structures like Segment Trees provide excellent performance but can be difficult to implement, modify, or extend with customized properties. We need a simpler layout that balances query speeds and update times without adding tree pointer overhead.

## My Approach
I implemented a **Square Root Decomposition** engine. Instead of organizing elements into a full binary hierarchy, the underlying array is divided into flat blocks of size approximately $\sqrt{N}$. Each block maintains a single precalculated total for the elements it contains.

Array:  [ 1, 5, 2 ] [ 4, 6, 1 ] [ 3, 5, 7 ] [ 10 ]
Block:    Block 0     Block 1     Block 2    Block 3
Sum:        8           11          15         10

1. **Updates ($O(1)$):** Modifying an element requires updating its index and adjusting its parent block's total by the difference. This bypasses structural tree steps entirely.
2. **Queries ($O(\sqrt{N})$):** For a range query $[L, R]$, the engine processes full intermediate blocks instantly using their precalculated values. It loops through individual elements only at the partial edges of the starting and ending blocks. Since there are at most $\sqrt{N}$ blocks and individual item checks are limited to the boundaries, the query time is securely bounded.

## Complexity Assessment
* **Point Modifications:** Constant $O(1)$ speed.
* **Interval Range Sums:** $\approx O(\sqrt{N})$ lookup passes.
* **Space Overhead:** Uses $O(\sqrt{N})$ extra memory to store the block totals.

This structure serves as the design foundation for advanced batch search architectures like **Mo's Algorithm**.