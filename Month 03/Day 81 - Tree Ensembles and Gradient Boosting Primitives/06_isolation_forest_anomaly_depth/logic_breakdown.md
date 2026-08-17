# Logic Breakdown: Isolation Forest Path Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Distance-based anomaly detection (like K-Nearest Neighbors) requires calculating Euclidean distances across all pairs of $O(N^2)$, which is computationally impossible for streaming big data. It also fails completely in high-dimensional space due to distance metric decay.

## My Approach
I encoded the mathematical primitives powering the **Isolation Forest**. Instead of measuring distance, this model attempts to *isolate* random samples by randomly selecting a feature and a random split value. 
Anomalies lie at the sparse edges of the dataset, meaning they get isolated extremely fast (short path length). Dense normal data requires dozens of random cuts to isolate a single point. I mapped the path length normalizer equation $c(n)$ using the Harmonic Number approximation, allowing the absolute tree depth to be translated into an actionable bounded probability score $[0, 1]$.

## Complexity Profile
* Runtime Bounds: $O(1)$ logarithmic floating-point approximation operations.
* Space Constraints: $O(1)$ absolute constant memory usage.