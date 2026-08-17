# Logic Breakdown: XGBoost Hessian Newton Step
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard Gradient Boosting only uses the first derivative (the gradient). This is equivalent to taking linear steps down a loss curve, which converges slowly and overshoots the minimum frequently if the curvature of the loss function is sharp.

## My Approach
I encoded the exact mathematical engine powering **XGBoost (Extreme Gradient Boosting)**. XGBoost evaluates the second-order Taylor expansion using both the Gradient ($g_i$) and the Hessian ($h_i$, the second derivative). By utilizing the formula $w^* = -\frac{\sum g_i}{\sum h_i + \lambda}$, the algorithm executes a **Newton-Raphson** step. It maps the true curvature (acceleration) of the loss space, jumping precisely to the optimal minimum in a single algorithmic pass while $\lambda$ imposes L2 structural regularization natively inside the leaf.

## Complexity Profile
* Runtime Bounds: $O(N)$ sequential array summation over the node samples.
* Space Constraints: $O(1)$ scalar execution isolated directly at the leaf level.