# Logic Breakdown: Spatial Pooling Primitives
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Deep networks extract thousands of feature maps. Keeping spatial dimensions (e.g., 224x224) intact through all layers causes exponential memory blowout. Moreover, exact pixel-perfect features cause models to fail if an object shifts slightly in the image frame.

## My Approach
I built completely vectorized Max and Average Pooling operators using matrix dimension splitting. By using `np.reshape(out_h, pool_size, out_w, pool_size)`, the 2D grid is mathematically folded into a 4D tensor representing the distinct $2 \times 2$ blocks. Applying `.max(axis=(1, 3))` instantly collapses the blocks, effectively halving the image resolution in constant C execution time.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution scaling optimally across native memory axes.
* Space Constraints: $O(1)$ memory view manipulation, allocating exclusively for the down-sampled final result matrix.