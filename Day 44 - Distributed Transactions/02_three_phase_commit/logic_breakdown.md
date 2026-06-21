# Logic Breakdown: Three-Phase Commit Protocol
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A standard 2PC setup can block indefinitely if the central coordinator crashes right after participants vote to commit. Nodes are left waiting in limbo, holding onto resource locks because they don't know the final decision.

## My Approach
I built a **Three-Phase Commit (3PC) State Matrix**.
By adding a tentative intermediate step called `PreCommit` between the initial vote and the final execution, the system removes this blocking risk. If a node times out waiting during this intermediate phase, it can safely assume the other nodes reached the same status and proceed with the commit, preventing stuck resource locks.

## Complexity Profile
* **Runtime Bounds:** Progression checks process in linear $O(N)$ time across $N$ nodes.
* **Space Constraints:** Operates safely within an $O(1)$ constant memory allocation model.