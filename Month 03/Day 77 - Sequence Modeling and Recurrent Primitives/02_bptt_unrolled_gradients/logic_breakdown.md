# Logic Breakdown: Backpropagation Through Time (BPTT)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Optimizing shared weights in an RNN requires attributing error back through previous time states. Using standard backpropagation only updates weights based on the current isolated time frame, ignoring temporal causality entirely.

## My Approach
I implemented the BPTT unrolled execution model. The sequence is processed in reverse (`reversed(range(len(X_seq))`). At each step $t$, the gradient error `dh_next` dictates how much the hidden state must adjust. Because weights are shared, we explicitly accumulate (`+=`) the partial derivatives `dW_xh` and `dW_hh` at every time step. 

*Note:* Because `dh_next` repeatedly multiplies by $W_{hh}^T \cdot (1 - \tanh^2(h_t))$, deep time sequences cause the gradient to multiply by values $<1$ repeatedly, driving the gradient to absolute zero (The Vanishing Gradient Problem).

## Complexity Profile
* Runtime Bounds: $O(T)$ matrix operations where $T$ is the total sequence length.
* Space Constraints: $O(1)$ memory usage beyond the cached forward pass hidden states.