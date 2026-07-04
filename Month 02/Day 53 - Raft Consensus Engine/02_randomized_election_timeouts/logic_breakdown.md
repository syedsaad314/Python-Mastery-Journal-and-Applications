# Logic Breakdown: Randomized Election Timeouts
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If multiple followers detect a missing leader simultaneously, they might all transition to candidates at the exact same moment. This creates a split-vote deadlock where no node wins a majority, halting cluster progress.

## My Approach
I introduced a randomized election timeout jitter ($T_{\text{timeout}} \in [150\text{ms}, 300\text{ms}]$). This ensures that one follower will always time out first, start its campaign, and claim leader status before its peers time out.

## Complexity Profile
* Runtime Bounds: Generating the randomized timeout runs in $O(1)$ steps.
* Space Constraints: Consumes standard $O(1)$ local heap variables.