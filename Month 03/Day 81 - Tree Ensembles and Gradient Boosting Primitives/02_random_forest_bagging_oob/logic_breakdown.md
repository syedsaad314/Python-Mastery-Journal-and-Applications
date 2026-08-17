# Logic Breakdown: Bagging & Out-Of-Bag Estimations
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Single decision trees overfit completely. To fix this, Random Forests build hundreds of trees, but giving every tree the exact same data produces highly correlated, identical models that fail to generalize.

## My Approach
I utilized **Bootstrap Aggregating (Bagging)** using `rng.integers()`. By drawing $N$ indices *with replacement*, the matrix naturally skips over certain indices. Mathematically, $\lim_{N\to\infty} (1 - \frac{1}{N})^N = \frac{1}{e} \approx 36.8\%$.
This means ~36.8% of the data naturally falls into the `oob_indices` array. We completely bypass the need for a separate train/test split—we train the tree on the `in_bag` matrix, and instantly cross-validate it on the isolated `oob` matrix without wasting any data.

## Complexity Profile
* Runtime Bounds: $O(N \log N)$ governed by the `np.setdiff1d` sorting operations isolating OOB indices.
* Space Constraints: $O(N)$ allocation for the bootstrap and set difference arrays.