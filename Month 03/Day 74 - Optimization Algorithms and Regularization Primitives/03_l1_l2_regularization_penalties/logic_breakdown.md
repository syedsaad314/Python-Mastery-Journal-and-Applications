# Logic Breakdown: L1 & L2 Regularization Penalties
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Highly parameterized models easily memorize the training set, leading to extreme weight magnitudes and complete predictive failure on new test data (Overfitting).

## My Approach
I vectorized two structural penalties integrated directly into the Loss Function. 
1. **L2 (Ridge) Regularization** adds the squared magnitude of weights ($\lambda \sum w^2$). Its derivative ($\lambda w$) gently shrinks large weights toward zero, distributing importance evenly.
2. **L1 (Lasso) Regularization** adds the absolute magnitude ($\lambda \sum |w|$). Its derivative uses `np.sign(w)`, which drives less-important feature weights to absolute zero, generating sparse models and performing intrinsic feature selection.

## Complexity Profile
* Runtime Bounds: $O(P)$ executing in constant hardware cycles over $P$ parameters.
* Space Constraints: $O(P)$ temporary allocation required to calculate derivative matrices.