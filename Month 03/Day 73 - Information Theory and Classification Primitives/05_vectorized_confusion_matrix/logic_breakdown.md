# Logic Breakdown: Vectorized Confusion Matrix
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Building a confusion matrix using Python `for` loops across a 10-million-row prediction set creates massive latency bottlenecks during model cross-validation.

## My Approach
I utilized index linearization and `np.bincount`. By calculating `y_true * num_classes + y_pred`, we compress a 2D mapping into a flat 1D hash value. `np.bincount` iterates over the underlying C array, tallying occurrences at the speed of the RAM bus. We then `.reshape()` the 1D count array back into the final $N \times N$ matrix.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution time over the prediction arrays.
* Space Constraints: $O(C^2)$ layout footprint where $C$ is the number of distinct classes.