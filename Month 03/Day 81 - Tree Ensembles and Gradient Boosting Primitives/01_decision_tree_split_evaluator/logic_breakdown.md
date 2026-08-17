# Logic Breakdown: Decision Tree Split Evaluator
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A decision tree algorithm (like CART) must dynamically determine exactly where to slice a continuous continuous variable array to segregate classes perfectly. Iterating through all possible points blindly without a mathematical anchor results in chaos.

## My Approach
I engineered the exact **Information Gain** metric utilizing the Gini Impurity formulation. 
$IG = Gini_{parent} - \left( \frac{N_{left}}{N} Gini_{left} + \frac{N_{right}}{N} Gini_{right} \right)$.
By applying a vectorized boolean mask (`features <= split_value`), the engine instantly branches the labels into Left and Right memory views. It calculates the weighted impurity drop; the algorithm is designed to scan across sorted feature arrays, constantly maximizing this Information Gain scalar to find the true structural partition line.

## Complexity Profile
* Runtime Bounds: $O(N)$ execution per proposed split evaluation threshold.
* Space Constraints: $O(N)$ memory required for holding the resulting boolean filter masks.