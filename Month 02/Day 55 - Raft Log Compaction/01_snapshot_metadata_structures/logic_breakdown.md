# Logic Breakdown: Snapshot Metadata Structures
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When old log entries are discarded, new or recovering nodes lose the historical context needed to validate incoming log updates. We need a way to store the exact position where the log was cut so nodes can still verify continuity.

## My Approach
I utilized an immutable `NamedTuple` to store the metadata. It captures the final log index (`last_included_index`) and its corresponding term (`last_included_term`), binding the data state to a specific point in the cluster's timeline.

## Complexity Profile
* Runtime Bounds: Reading metadata attributes runs in $O(1)$ constant time.
* Space Constraints: Memory overhead scales at $O(D)$, where $D$ represents the size of the state data dictionary.