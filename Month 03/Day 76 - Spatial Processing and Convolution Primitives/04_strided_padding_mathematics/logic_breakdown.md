# Logic Breakdown: Strided Padding Mathematics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard sliding window convolutions aggressively "eat" the borders of an image (e.g., a $5 \times 5$ image with a $3 \times 3$ kernel shrinks to $3 \times 3$). Continuous shrinkage causes deep networks to instantly collapse input dimensions down to $1 \times 1$ before features are fully mapped.

## My Approach
I utilized `np.pad` to execute border zero-padding, wrapping the spatial tensor in a neutralizing halo of zeroes. I also implemented the foundational spatial shape formula: $O = \lfloor\frac{W - K + 2P}{S}\rfloor + 1$. By configuring $P = \frac{K - 1}{2}$, the operation is guaranteed to perform "Same Padding," preserving spatial volume identically across hidden layers.

## Complexity Profile
* Runtime Bounds: $O(N)$ memory shifting execution via internal array boundaries.
* Space Constraints: $O((H+2P) \cdot (W+2P))$ memory allocation to construct the slightly larger padded wrapper matrix.