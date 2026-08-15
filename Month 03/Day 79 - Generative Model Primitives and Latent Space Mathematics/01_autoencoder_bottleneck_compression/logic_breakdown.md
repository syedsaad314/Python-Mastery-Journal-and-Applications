# Logic Breakdown: Autoencoder Bottleneck Compression
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a neural network maps 100 inputs to 100 outputs directly, it simply learns the identity function ($f(x) = x$) by copying the data, failing to extract any underlying semantic understanding or patterns.

## My Approach
I implemented a structural "hourglass" bottleneck. The Encoder matrices forcefully squeeze $100$ dimensional data into a $10$ dimensional latent vector `z`. To successfully rebuild the original data from `z` via the Decoder, the network is mathematically forced to discard noise and isolate only the absolute principal components and semantic features of the data. 

## Complexity Profile
* Runtime Bounds: $O(B \cdot N_{in} \cdot N_{latent})$ dictated by the matrix dot products.
* Space Constraints: $O(B \cdot N_{latent})$ for holding the compressed representation in memory.