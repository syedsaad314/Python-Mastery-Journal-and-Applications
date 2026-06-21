# Logic Breakdown: Write-Ahead Logging Integrity
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a database node modifies its live memory values first and crashes right before saving the log to storage, its in-memory changes are lost on restart, leading to corrupted data states.

## My Approach
I implemented a structural **Write-Ahead Logging (WAL) System**.
The node forces state transitions to save to persistent storage *before* updating any values in runtime memory. If the system crashes midway through an operation, the restart routine reads the log to replay completed writes and clean up half-finished updates.

## Complexity Profile
* **Runtime Bounds:** Appending log rows to persistent storage executes in $O(1)$ constant time.
* **Space Constraints:** Storage size scales linearly at $O(A)$ relative to total operational events $A$.