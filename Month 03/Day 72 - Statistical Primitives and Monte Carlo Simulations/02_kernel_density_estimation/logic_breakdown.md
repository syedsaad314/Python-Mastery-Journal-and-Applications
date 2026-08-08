# Logic Breakdown: Kernel Density Estimation (KDE)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Histograms suffer from bin-width bias, forcing discrete blocky views of continuous data. Deriving a smooth continuous distribution from discrete data points using double `for` loops $O(M \times N)$ is computationally crippling.

## My Approach
I utilized NumPy broadcasting to compute the pairwise distances between every evaluation point and every observed data point simultaneously (`x_eval[:, np.newaxis] - data[np.newaxis, :]`). A Gaussian kernel function is applied to this $M \times N$ difference matrix. Summing across the observed points yields the smooth density curve instantaneously.

## Complexity Profile
* Runtime Bounds: $O(M \cdot N)$ executing entirely within compiled C subroutines without Python GIL overhead.
* Space Constraints: $O(M \cdot N)$ memory allocation required for the pairwise distance broadcasting matrix.