# Logic Breakdown: Naive RNN Hidden State
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Standard Feed-Forward Networks assume all inputs (and outputs) are independent of each other. If processing time-series data or sentences, the network must maintain temporal memory of previously seen inputs to provide context for the current input.

## My Approach
I engineered a recursive hidden state primitive. The engine updates an internal vector $h_t$ at every time step $t$. It fuses the current input $x_t$ with the preceding historical memory $h_{t-1}$ using matrix addition, squashed by a `tanh` nonlinearity. By sharing identical weights ($W_{xh}, W_{hh}$) across all time steps, the network generalizes sequential patterns regardless of total sequence length.

## Complexity Profile
* Runtime Bounds: $O(T \cdot H^2)$ where $T$ is the number of time steps and $H$ is the hidden state dimensionality.
* Space Constraints: $O(T \cdot H)$ to cache the history of hidden states for the backward pass.