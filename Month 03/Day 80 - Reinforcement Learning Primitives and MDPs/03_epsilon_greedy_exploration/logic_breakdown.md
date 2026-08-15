# Logic Breakdown: Epsilon-Greedy Exploration
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If an RL agent always exploits the best known action immediately (Greedy Policy), it gets trapped in local minimums early in training, forever ignoring other paths that might yield significantly higher long-term rewards. 

## My Approach
I mapped the **Epsilon-Greedy** trade-off primitive. The algorithm rolls a random number; if it falls beneath $\epsilon$, the agent overrides its knowledge and selects randomly (Explore). Otherwise, it takes the mathematical max (Exploit). 
Crucially, I implemented exponential decay: $\epsilon_{t+1} = \epsilon_t \times \text{decay}$. The agent starts completely chaotic ($\epsilon=1.0$) to map the environment, and smoothly shifts into pure exploitation ($\epsilon \rightarrow 0.01$) as its Q-Table mathematically hardens towards the true optimal values.

## Complexity Profile
* Runtime Bounds: $O(A)$ dictated by `np.argmax()` across the action space matrix array.
* Space Constraints: $O(1)$ scalar tracking for random value generators and epsilon persistence.