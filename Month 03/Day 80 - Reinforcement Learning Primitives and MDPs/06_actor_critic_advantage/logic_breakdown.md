# Logic Breakdown: Advantage Function (Actor-Critic)
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Vanilla Policy Gradients (REINFORCE) suffer from extreme variance. If a trajectory is generally good, the math pushes *all* action probabilities up—even the bad ones inside that trajectory. The network lacks a "baseline" of what is objectively good versus what is just expected.

## My Approach
I mathematically unified the Actor (Policy) and Critic (Value) networks via the Advantage Function: $A_t = R_t + \gamma V(S_{t+1}) - V(S_t)$. 
Instead of multiplying the policy loss by the raw absolute reward, we multiply it by the Advantage. If the Agent takes an action that yields $10$, but the Critic *expected* $10$, the Advantage is $0$; the policy weights are not updated, because the agent simply did what was predicted. If it gets $10$ but expected $2$, the Advantage is $+8$, driving massive positive probability shifts. This neutralizes variance and accelerates convergence dynamically.

## Complexity Profile
* Runtime Bounds: $O(T)$ operating a strict linear trajectory pass to calculate TD-errors.
* Space Constraints: $O(T)$ storing isolated advantage delta scalars prior to gradient chaining.