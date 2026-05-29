# Logic Breakdown: Mutex Lock Synchronization
**Engineer:** Syed Saad Bin Irfan

## The Problem
To prevent concurrent data corruption on shared resources, we need a way to restrict block access to a single thread at a time.

## My Approach
I implemented a **Mutex Lock** using Python's `threading.Lock`. By wrapping the modification steps inside a `with self.mutex:` context manager, the executing thread secures exclusive access to that code block. Any other thread attempting to run this logic is paused and placed into a wait queue until the lock is released, ensuring data integrity.

## Complexity Profile
* **Runtime Bounds:** $O(N)$ execution times, introducing slight lock-wait latency overhead.
* **Space Constraints:** $O(N)$ thread tracking layout.