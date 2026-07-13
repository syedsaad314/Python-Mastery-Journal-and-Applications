# Logic Breakdown: Automated Reverse Compensating Transaction Rollback
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Because the Saga pattern commits local microservice changes instantly, you can't just use a standard database rollback to wipe out a multi-service failure. Instead, you have to actively apply balancing actions (like refunding a charge or releasing a stock hold) to bring everything back into a consistent state.

## My Approach
I built a reverse-order cleanup coordinator. It pulls the names of successful steps out of the history buffer and runs their matching compensation functions backward. This undoes mutations in the exact reverse order they were applied, preventing architectural deadlocks.

## Complexity Profile
* Runtime Bounds: Processing rollbacks runs in $O(K)$ time, where $K$ is the number of finished steps that need undoing.
* Space Constraints: Allocates memory at $O(K)$ to track the rollback results.