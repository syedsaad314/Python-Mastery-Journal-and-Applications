# Logic Breakdown: Eigenvalue Decomposition (PCA Foundation)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
To perform Principal Component Analysis (PCA) manually, we must mathematically identify the specific vectors (axes) across which our data features exhibit the most variance.

## My Approach
I used `np.linalg.eigh()` on the dataset's Covariance Matrix. Because covariance matrices are symmetric, `eigh` is mathematically guaranteed to produce real eigenvalues and orthogonal eigenvectors faster and more stably than standard `eig`. The eigenvectors represent the principal axes, and the eigenvalues denote the magnitude of variance along those axes.

## Complexity Profile
* Runtime Bounds: $O(F^3)$ where $F$ is the number of features, dictated by the eigendecomposition step.
* Space Constraints: $O(F^2)$ to store the dense covariance matrix and resulting eigenvector matrix.