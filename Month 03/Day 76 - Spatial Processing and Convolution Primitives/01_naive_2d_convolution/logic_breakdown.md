# Logic Breakdown: Naive 2D Convolution Primitive
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Applying a feature-extraction filter (e.g., edge detection) across an image requires taking a small weight matrix (the kernel) and sliding it pixel-by-pixel across the input. Operating this via nested `for` loops in Python destroys processing speed. 

## My Approach
I implemented the mathematical cross-correlation logic directly. The window bounds (`i_h - f_h + 1`) guarantee the kernel never slides out of the memory boundaries. While this naive nested looping structure reveals the exact elemental arithmetic of the convolution operation, it proves definitively why we need matrix unrolling (im2col) for real-world Deep Learning pipelines.

## Complexity Profile
* Runtime Bounds: $O(N \cdot M \cdot K \cdot L)$ heavily constrained by Python loop interpreting across spatial height/width and filter sizes.
* Space Constraints: $O(H_{out} \cdot W_{out})$ static boundary allocation for the feature map result.