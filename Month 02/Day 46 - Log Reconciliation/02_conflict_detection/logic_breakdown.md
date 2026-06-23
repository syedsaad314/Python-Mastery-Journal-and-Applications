# Logic Breakdown: Log Conflict Detection
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When network partitions heal, followers often bring conflicting uncommitted entries from old terms that must be proactively flagged for resolution.

## My Approach
I engineered a linear term comparison scanner. It iterates simultaneously through the leader's and follower's logs to find the first index where their term tracking variables disagree, marking the exact starting point of data conflict.

## Complexity Profile
* Runtime Bounds: Scales linearly at $O(M)$ where $M$ is the minimum length of the logs compared.
* Space Constraints: Maintains strict constant memory footprints of $O(1)$.