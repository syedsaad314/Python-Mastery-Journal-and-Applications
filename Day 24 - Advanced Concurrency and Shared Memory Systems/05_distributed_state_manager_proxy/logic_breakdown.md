# Logic Breakdown: Centralized State Management via Process Proxy Managers
**Engineer:** Syed Saad Bin Irfan

## The Problem
Directly sharing complex data structures (like multi-level nested dictionaries or objects) across processes usually requires writing complex, low-level binary lock systems from scratch.

## My Approach
I utilized Python's high-level `multiprocessing.managers.SyncManager` to handle state synchronization automatically.

The manager spins up a dedicated background process that owns the real data object, and returns lightweight **Proxy Wrappers** to the other worker processes. When a process alters the proxy dictionary, the proxy forwards the mutation request over a local socket connection to the master process behind the scenes, ensuring safe, synchronized state updates across all workers.

## Complexity Profile
* **Runtime Bounds:** Network proxy synchronization adds minor network overhead, running in $O(1)$ atomic lookups.
* **Space Constraints:** Scales at $O(K)$ space where $K$ counts overall state keys added.