# Logic Breakdown: Shannon Entropy
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Decision Trees need a mathematical metric to evaluate how "good" a dataset split is. If we split data and the resulting nodes are perfectly homogenous, we need a metric that registers as zero uncertainty.

## My Approach
I implemented Claude Shannon's Information Entropy: $H(X) = -\sum p(x) \log_2 p(x)$. By calling `np.unique(return_counts=True)`, the engine rapidly tallies class frequencies in C. The vectorized logarithm then scales the probabilities, yielding the required bits of information needed to encode the dataset's state.

## Complexity Profile
* Runtime Bounds: $O(N \log N)$ governed by the `np.unique` sorting pass over $N$ items.
* Space Constraints: $O(C)$ where $C$ is the number of unique classes dynamically allocated for counts.