# Logic Breakdown: InfoNCE Contrastive Loss
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Models like CLIP embed images and text into a shared latent space. Since there are no explicit "classes", standard Cross-Entropy fails. The network must be taught to pull corresponding text/image pairs together while pushing *all other combinations in the batch* infinitely far apart.

## My Approach
I utilized the **InfoNCE (Information Noise-Contrastive Estimation) Loss**. 
First, I perform $L2$ Normalization. Doing `np.dot` on normalized vectors computes exact Cosine Similarities across the entire batch $N \times N$ instantly. 
The diagonal of this matrix represents the "Positive" pairs (Image 1 $\rightarrow$ Text 1). Every other cell is a "Negative" pair. By evaluating symmetric Cross-Entropy directly on the scaled similarity matrix, the loss penalizes the network heavily if the diagonal similarities aren't significantly higher than all off-diagonal interactions.

## Complexity Profile
* Runtime Bounds: $O(B^2 \cdot D)$ driven by the dense batch-to-batch matrix dot products.
* Space Constraints: $O(B^2)$ holding the complete contrastive similarity logit matrix.