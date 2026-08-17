# Logic Breakdown: Gradient Boosting Residual Matcher
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Random Forests build trees independently and average them. However, averaging cannot fix systemic bias. If the ensemble continuously under-predicts a specific edge-case feature, adding 100 more parallel trees won't solve the structural blindness.

## My Approach
I implemented the core **Sequential Additive** logic of Gradient Boosting Machines (GBM). Instead of predicting the target $y$ directly, subsequent trees are strictly tasked with predicting the *residual error* ($y - \hat{y}$) of the current ensemble. Mathematically, this residual is the exact negative gradient of the Mean Squared Error loss function $\left(-\frac{\partial L}{\partial F(x)}\right)$. We are executing Gradient Descent in function space rather than parameter space.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution to compute negative gradients over predictions.
* Space Constraints: $O(N)$ intermediate allocation layout for the continuous residual array.