# Logic Breakdown: Exploding Gradient Clipping
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
While vanishing gradients stall networks, "Exploding Gradients" obliterate them. If gradients repeatedly multiply by values $>1$ during deep BPTT unrolls, they quickly exceed IEEE `float64` boundaries, instantly corrupting all weights with `NaN` (Not a Number) values.

## My Approach
I utilized Global L2 Norm Clipping. Instead of blindly capping individual matrix values (which alters the physical direction of the gradient vector step), the engine calculates the global vector length (L2 norm) across all network layers simultaneously. If the total length exceeds `max_norm`, the engine scales *every* parameter down by the exact same ratio ($\frac{max\_norm}{global\_norm}$). This shrinks the step size without changing the directional angle of descent.

## Complexity Profile
* Runtime Bounds: $O(P)$ sequential pass over $P$ total network parameters.
* Space Constraints: $O(1)$ memory allocation; scales matrices directly in-place.