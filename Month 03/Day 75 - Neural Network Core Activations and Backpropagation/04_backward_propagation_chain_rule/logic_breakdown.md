# Logic Breakdown: Backward Propagation Calculus
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
To optimize a network, we need to know exactly how much a change in a specific weight $W$ deep in the network impacts the final Loss $L$. Calculating this manually without utilizing localized partial derivatives causes numerical chaos.

## My Approach
I implemented the core computational heart of Deep Learning: The Chain Rule of Calculus over matrices. 
When the upstream gradient $dZ$ arrives from the activation layer ahead of it, the engine calculates the localized partial derivatives:
1. $dW^{[l]} = \frac{\partial \mathcal{L}}{\partial W^{[l]}} = \frac{1}{m} dZ^{[l]} A^{[l-1] T}$
2. $db^{[l]} = \frac{\partial \mathcal{L}}{\partial b^{[l]}} = \frac{1}{m} \sum dZ^{[l]}$
3. $dA^{[l-1]} = W^{[l] T} dZ^{[l]}$ (This specific output is tossed backward down the chain to the previous layer).

## Complexity Profile
* Runtime Bounds: $O(N_{out} \cdot N_{in} \cdot M)$ matrix multiplication runtime bounds.
* Space Constraints: $O(N_{out} \cdot N_{in})$ localized temporary gradient allocation overhead.