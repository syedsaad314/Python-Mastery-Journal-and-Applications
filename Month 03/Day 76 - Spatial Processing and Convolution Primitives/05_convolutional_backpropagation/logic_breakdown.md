# Logic Breakdown: Convolutional Backward Propagation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Updating filter matrices during neural network training requires mapping an incoming localized gradient array ($dZ$) backward across the spatial receptive fields without violating spatial calculus boundaries.

## My Approach
I unrolled the spatial chain rule into two exact mathematical operations:
1. **$dW$ Calculation:** The gradient of the loss with respect to the weights is derived by sliding the upstream gradient error $dZ$ across the raw input activations $A_{prev}$ (Valid Cross-Correlation).
2. **$dA_{prev}$ Calculation:** The gradient passed backwards to previous layers is computed by padding $dZ$ intensely, rotating the weight kernel 180 degrees (`np.rot90`), and executing a Full Convolution. This mathematically correctly distributes the error back to every pixel that contributed to the forward output.

## Complexity Profile
* Runtime Bounds: $O(I_H \cdot I_W \cdot K_H \cdot K_W)$ limited locally due to naive loop implementation.
* Space Constraints: $O(I_H \cdot I_W)$ allocation bounds to map the backward partial derivative cache matrices.