# Logic Breakdown: Bellman Optimality (Value Iteration)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
An AI agent moving through an environment must evaluate not just the immediate reward of an action, but the infinite chain of consequences that follow it. Calculating this manually via a branching tree generates infinite loop traps and exponential computational blowouts.

## My Approach
I implemented the Bellman Optimality Equation via Value Iteration. By asserting $V(s) = \max_a [ R(s, a) + \gamma \sum P(s'|s,a)V(s') ]$, we mathematically truncate the infinite future using dynamic programming. The algorithm computes the expected value of taking a step into the next state, discounted by $\gamma$, iteratively sweeping the state space until the values mathematically converge to a stationary equilibrium.

## Complexity Profile
* Runtime Bounds: $O(I \cdot S^2 \cdot A)$ where $S$ is states, $A$ is actions, and $I$ is iterations until convergence.
* Space Constraints: $O(S)$ independent memory allocation for the state Value array.