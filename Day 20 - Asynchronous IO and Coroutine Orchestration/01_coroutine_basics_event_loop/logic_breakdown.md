# Logic Breakdown: Coroutine Basics and Event Loop Integration
**Engineer:** Syed Saad Bin Irfan

## The Problem
Traditional synchronous code locks the entire thread when waiting for network operations, wasting CPU cycles. We need a way to pause long-running I/O tasks and pass control to other code blocks without thread context-switching overhead.

## My Approach
I implemented cooperative multitasking using Python's `asyncio` runtime. 

By defining functions with `async def`, they compile into native coroutine objects instead of immediate execution blocks. When a coroutine hits an `await` statement, it explicitly yields control back to the central event loop. While the simulated network delay processes in the background, the event loop runs other tasks on the same thread, optimizing resource utilization.

## Complexity Profile
* **Runtime Bounds:** $O(1)$ lookup operations; overall runtime matches the single longest background delay rather than their sum.
* **Space Constraints:** Constant $O(1)$ memory mapping space overhead to track active coroutine execution frames.