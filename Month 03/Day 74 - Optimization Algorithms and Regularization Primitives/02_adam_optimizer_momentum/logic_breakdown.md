# Logic Breakdown: Adam Optimizer Primitive
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard Gradient Descent gets trapped in saddle points and oscillates wildly in narrow ravines. Furthermore, using a single global learning rate for all parameters causes sparse features to learn far too slowly.

## My Approach
I implemented the Adaptive Moment Estimation (Adam) algorithm directly into NumPy array logic. Adam combines Momentum (first moment, $m_t$) to push through saddle points, and RMSProp (second moment, $v_t$) to adapt the learning rate per parameter. The bias-correction mechanism ($\hat{m}$ and $\hat{v}$) stabilizes the algorithm during the initial steps where the momentum arrays are mostly zero.

## Complexity Profile
* Runtime Bounds: $O(P)$ executing vectorized hardware math over $P$ parameters.
* Space Constraints: $O(P)$ persistent memory required to track the $m$ and $v$ momentum arrays.