# Logic Breakdown: Clock Drift Boundary Protection
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Relying on physical wall-clock time across different physical servers is dangerous. If a leader's clock runs slower than its followers' clocks, its lease might look valid locally even though the followers have already timed out and started a new election.

## My Approach
I engineered a conservative fallback calculation layer. It takes the nominal lease duration and reduces it by a configurable maximum clock drift percentage ($Drift_{max}$). By cutting the lease short on the leader's side, we create a safety buffer that prevents stale reads even if the system clocks drift.

## Complexity Profile
* Runtime Bounds: Math execution calculations take $O(1)$ constant time steps.
* Space Constraints: Simple scalar updates scaling at constant $O(1)$ footprint spaces.