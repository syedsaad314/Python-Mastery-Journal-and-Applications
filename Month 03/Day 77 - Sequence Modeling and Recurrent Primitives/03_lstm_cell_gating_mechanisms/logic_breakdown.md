# Logic Breakdown: LSTM Cell Gating Mechanisms
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Naive RNNs fail on long sequences because repetitive multiplication causes derivatives to vanish. We need a mathematical primitive capable of maintaining long-term state across hundreds of time steps without degradation.

## My Approach
I modeled the exact LSTM Cell architecture. I optimized execution by calculating all four internal gates (`Forget`, `Input`, `Candidate`, `Output`) via a single massive matrix multiplication (`np.dot(W, concat_in)`), then splicing the output array. 

The breakthrough is the Cell State ($C_t$). Because $C_t = f_t * C_{t-1} + i_t * \tilde{C}_t$ uses **element-wise addition** rather than matrix multiplication, gradients flow completely unobstructed backward through time (acting as a "Constant Error Carousel"), entirely mitigating the vanishing gradient penalty.

## Complexity Profile
* Runtime Bounds: $O((H + X) \cdot 4H)$ where $H$ is hidden size and $X$ is input size.
* Space Constraints: $O(H)$ overhead for maintaining the auxiliary Cell State $C_t$.