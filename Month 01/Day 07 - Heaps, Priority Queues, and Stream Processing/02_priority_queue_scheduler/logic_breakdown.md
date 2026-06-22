# Logic Breakdown: Task Scheduling via Priority Queues
**Engineer:** Syed Saad Bin Irfan

## The Problem
Standard First-In, First-Out (FIFO) queues process background requests in the exact order they arrive. However, if a critical system alert (like a core database disconnection) gets stuck behind hundreds of low-priority tasks (like user tracking events), the entire application can crash. We need a routing engine that balances incoming logs and immediately surfaces high-priority payloads.

## My Approach
I built a task processing broker backed by an optimized min-priority heap. To keep sorting stable when two tasks share the exact same priority level, I added a progressive counter (`sequence_counter`) into the data tuples. This design ensures that ties are resolved fairly, following standard chronological arrival order.

## Critical Thinking
*   **Time Complexity:** Adding a task takes $O(\log N)$ time, and pulling the next job for execution runs in $O(\log N)$ time.
*   **Space Complexity:** Scales linearly at $O(N)$ relative to the total number of items currently waiting in the processing queue.

This architecture prevents low-priority data congestion, ensuring that time-critical processes skip the line and execute without delay.