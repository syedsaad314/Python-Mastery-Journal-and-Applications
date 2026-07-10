# Logic Breakdown: Participant State Durability Simulation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a participant node votes YES to commit a transaction but then crashes before the coordinator can send the final commit command, that node must remember its vote after rebooting. It cannot lose track of its promise to the coordinator.

## My Approach
I built a write-ahead logging (WAL) simulator. Before confirming its vote back to the coordinator, the node appends a `PREPARE_LOG` string entry to its durable history log. This record guarantees the transaction can be safely recovered or rolled back even after sudden node restarts.

## Complexity Profile
* Runtime Bounds: Appending to the log and updating the prepared cache takes constant time $O(1)$.
* Space Constraints: Memory overhead scales linearly ($O(T)$) based on the number of processed transactions.