# Logic Breakdown: Two-Phase Commit Blocking Anomaly Simulator
**Engineer:** Syed Saad Bin Irfan

## The Problem
The biggest vulnerability of the Two-Phase Commit protocol is that it is a **blocking protocol**. If the coordinator crashes right after participants vote to prepare, those participants cannot make a decision on their own. They must keep their resource locks active indefinitely, which can grind the system to a halt.

## My Approach
I built a simulation showing this **Hanging State Blocking Anomaly**.

When a participant node votes to commit, it enters the `PREPARED` state and locks its resources. If the coordinator goes offline before sending the final commit or abort instruction, the participant node is stuck. It cannot safely abort (because other nodes might have committed) and it cannot safely commit (because other nodes might have aborted). It has no choice but to block and wait for the coordinator to recover.

## Complexity Profile
* **Runtime Bounds:** Timeout evaluations run in $O(1)$ constant execution time.
* **Space Constraints:** Uses $O(1)$ constant internal space to track state attributes.