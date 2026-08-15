# Logic Breakdown: Q-Learning Temporal Difference
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Value Iteration requires perfect knowledge of the environment's transition probabilities ($P$). In real-world reinforcement learning (like autonomous driving), the agent does not possess a map of how the world reacts; it must learn "Model-Free" by experiencing it.

## My Approach
I utilized the **Q-Learning Temporal Difference (TD) Error**. When the agent takes a step, it compares its previous hypothesis ($Q_{current}$) to what actually just happened plus its new vantage point ($\text{Reward} + \gamma \max Q_{next}$). The difference between reality and the hypothesis is the TD Error. By multiplying this error by a learning rate ($\alpha$), the Q-matrix inches closer to the true optimal policy purely through experiential stochastic sampling.

## Complexity Profile
* Runtime Bounds: $O(1)$ constant time execution to lookup and update a specific matrix coordinate.
* Space Constraints: $O(S \cdot A)$ maintaining the full Q-value historical state-action matrix.