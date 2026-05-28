# Logic Breakdown: Remote Procedure Call (RPC) Internals
**Engineer:** Syed Saad Bin Irfan

## The Problem
In distributed environments, forcing systems to handle raw network routes manually can clutter business logic. We need an abstraction layer that allows code on one machine to execute functions on another machine seamlessly.

## My Approach
I built a lightweight, extensible RPC dispatch layer that mimics the JSON-RPC 2.0 communication format. 

The framework maps function references directly inside an internal registry dictionary. When a serialized network payload arrives, the dispatch engine extracts the target method name and arguments, unpacked using standard Python parameter unpacking (`*args`, `**kwargs`), executes the logic safely, and bundles the result back into a structured JSON string.

## Complexity Profile
* **Runtime Bounds:** Calls resolve in $O(1)$ registry retrieval time, plus the execution cost of the underlying function.
* **Space Constraints:** Bounded at $O(M)$ where $M$ matches total registered procedures in the routing map.