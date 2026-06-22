# Logic Breakdown: Non-Consecutive State Decisions
**Engineer:** Syed Saad Bin Irfan

## The Problem
In scheduling or asset management, you frequently run into situations where choosing an item forces you to skip its immediate neighbors (such as avoiding back-to-back server maintenance tasks or selecting high-yield real estate plots under zoning limits). Finding the best overall path requires tracking the long-term impact of skipping versus choosing at every single step.

## My Approach
I built a linear state machine that acts like an Include/Exclude toggle. As the engine steps through the options, it calculates two paths: it can either skip the current item and carry forward the maximum profit found so far (`include_past_node_max`), or choose the current item and add its value to the profit from two steps back (`skip_past_node_max + current_asset`). The engine takes the maximum of these two paths, updating its state smoothly with constant memory.

## Critical Thinking
*   **Time Complexity:** Processes the entire sequence in a clean, linear $O(N)$ runtime pass.
*   **Space Complexity:** Optimized down to a flat $O(1)$ constant footprint using simple tracking registers.

This lightweight state switching strategy is incredibly efficient for live asset selection pipelines, maximizing returns without burning through system memory.