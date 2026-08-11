# Logic Breakdown: Affine Transform Forward Pass
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A dense neural layer must connect every input feature to every output neuron across an entire batch of data simultaneously. Using sequential nested iteration across neurons and batches cripples model training efficiency.

## My Approach
I expressed the dense layer operation strictly as a linear algebra Affine Transformation: $Z^{[l]} = W^{[l]} A^{[l-1]} + b^{[l]}$. 
By organizing the inputs into columnar batches, `np.dot()` invokes the low-level C BLAS library to perform the full feature-to-neuron sum product in a single heavily parallelized hardware pass. The bias $b$ is automatically broadcast across the batch dimension.

## Complexity Profile
* Runtime Bounds: $O(N_{out} \cdot N_{in} \cdot M)$ where $M$ is batch size, optimally computed using SIMD pipelines.
* Space Constraints: $O(N_{out} \cdot M)$ to allocate the output $Z$ matrix.