# Logic Breakdown: Gini Impurity Evaluator
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
While Shannon Entropy provides exact information bit tracking, calculating `log2` across millions of split candidates during Random Forest training imposes heavy CPU floating-point limits.

## My Approach
I implemented the Gini Impurity calculation: $1 - \sum p_i^2$. Because computing mathematical squares is significantly faster at the hardware level than computing logarithms, Gini provides near-identical decision tree splitting performance but executes in fewer CPU cycles.

## Complexity Profile
* Runtime Bounds: $O(N \log N)$ heavily dominated by the unique value sort boundary.
* Space Constraints: $O(C)$ to map the internal class count distribution bins.