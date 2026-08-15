# Logic Breakdown: Discounted Rewards-to-Go
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
In environments with sparse rewards (e.g., Chess, where reward only happens at Checkmate), the agent must learn that early actions were highly valuable. Computing $\sum \gamma^k R_{t+k}$ manually at every individual step $t$ executes in $O(T^2)$ time, generating massive delays for long sequences.

## My Approach
I optimized the sequence into a reversed recursive accumulator: $G_t = R_t + \gamma G_{t+1}$. By iterating backward through the chronological episode data, we maintain a `running_add` variable that decays by $\gamma$ at each step, propagating the delayed reward backward through time. This converts an $O(T^2)$ operation into a strict $O(T)$ linear pass.

## Complexity Profile
* Runtime Bounds: $O(T)$ single reverse sequence loop across the episode timeline.
* Space Constraints: $O(T)$ contiguous array allocation to hold the mapped trajectory returns.