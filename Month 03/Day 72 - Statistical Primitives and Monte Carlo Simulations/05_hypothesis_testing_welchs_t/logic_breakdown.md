# Logic Breakdown: Welch's T-Test Primitive
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Assuming equal variances between different datasets (Student's t-test) causes severe Type I errors (false positives) in real-world hypothesis testing where group spreads vary wildly.

## My Approach
I implemented the pure mathematical equations for Welch's T-Test directly into NumPy vector primitives. Instead of relying on a black-box package, breaking out the numerator, standard error denominator, and the Welch-Satterthwaite degrees of freedom equation directly leverages high-speed C arrays. 

## Complexity Profile
* Runtime Bounds: $O(N_a + N_b)$ where lengths represent the respective group arrays.
* Space Constraints: $O(1)$ memory allocation independent of the initial sampling array sizes.