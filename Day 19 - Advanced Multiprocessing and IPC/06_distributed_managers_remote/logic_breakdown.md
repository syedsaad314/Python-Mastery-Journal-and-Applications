# Logic Breakdown: Shared State via BaseManager
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard multiprocessing shared memory structures are limited to basic C-type primitives or flat arrays. Sharing custom class instances or objects across separate processes requires an advanced synchronization pattern.

## My Approach
I built a centralized network abstraction using `multiprocessing.managers.BaseManager`. 

By registering my custom `MetricsStateTracker` class with the manager, the system creates a central coordination server. Other processes interact with this state tracker via proxy objects that forward method calls over local network sockets behind the scenes, allowing seamless object manipulation across process boundaries.

## Complexity Profile
* **Runtime Bounds:** Network proxy communication adds a small socket serialization overhead to method lookups.
* **Space Constraints:** Data storage is centralized inside the main manager server footprint.