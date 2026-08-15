# Logic Breakdown: REINFORCE Policy Gradient (Log-Derivative)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Value-based methods (Q-Learning) break down entirely in continuous action spaces (e.g., steering wheel angles). We need a method to train a neural network to directly output an action probability distribution ($\pi_\theta$) without modeling a Q-Table.

## My Approach
I translated the REINFORCE theorem into NumPy calculus. The mathematical objective is to maximize $J(\theta) = \mathbb{E}[R(\tau)]$. Through the Log-Derivative trick ($\nabla_\theta \log \pi(a|s)$), the engine computes the gradient explicitly as: Loss $= -\sum \log(\pi(a|s)) \times G_t$. 
If an action resulted in a high positive reward-to-go ($G_t$), the negative log loss violently pulls the network weights to increase that action's probability next time. If $G_t$ is negative, it suppresses it.

## Complexity Profile
* Runtime Bounds: $O(T)$ executing dot products directly across episode trajectories.
* Space Constraints: $O(T)$ intermediate allocations required for generating log probability vectors.