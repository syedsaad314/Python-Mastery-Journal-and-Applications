# Logic Breakdown: Jaccard Similarity (IoU)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When evaluating object detection bounding boxes or semantic segmentation models, standard accuracy metrics fail entirely because background pixels overwhelm the foreground target features (Class Imbalance).

## My Approach
I utilized Intersection over Union (IoU) modeled through binary bitwise operators (`np.logical_and`, `np.logical_or`). Instead of rewarding the model for correctly predicting the massive empty background, Jaccard strictly penalizes false positives and false negatives by measuring only the overlap of active prediction pixels against ground-truth pixels.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution speed over the unrolled binary vectors.
* Space Constraints: $O(N)$ intermediate allocation required to evaluate boolean masks.