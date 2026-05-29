# Logic Breakdown: Thread Lifecycles and Shared State Race Conditions
**Engineer:** Syed Saad Bin Irfan

## The Problem
Python instructions like `self.value += 1` look atomic but compile down to multiple underlying bytecode steps (Load, Modify, Store). When multiple threads manipulate this variable concurrently, the OS thread scheduler can interrupt a thread mid-cycle, causing it to overwrite stale data and corrupt state.

## My Approach
I built an un-synchronized counter system to isolate this exact behavior. By forcing a brief sleep (`time.sleep`) right between the retrieval and assignment stages, I exposed the race condition. This demonstrates how threads read identical values before completing their updates, resulting in missing increments and data loss.

## Complexity Profile
* **Runtime Bounds:** $O(N)$ where $N$ matches total thread assignments.
* **Space Constraints:** $O(N)$ thread stack context allocation parameters.