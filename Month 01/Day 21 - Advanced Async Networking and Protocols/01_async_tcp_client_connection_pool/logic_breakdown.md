# Logic Breakdown: Async TCP Connection Pooling Simulation
**Engineer:** Syed Saad Bin Irfan

## The Problem
Opening and closing TCP connections repeatedly for every payload introduces significant network handshake latency and taxes OS file descriptors. We need a way to reuse active network streams across concurrent tasks.

## My Approach
I built an asynchronous connection pool using a bounded `asyncio.Queue`. 

The pool pre-allocates connection proxies during startup. When a concurrent task needs a connection, it calls `await pool.get()`. If all connections are leased out, the task pauses without blocking the event loop until another worker calls `pool.put()` to return its connection pair.

## Complexity Profile
* **Runtime Bounds:** Lease and release operations run in constant $O(1)$ time.
* **Space Constraints:** Bounded to $O(K)$ space, where $K$ is the maximum configured pool capacity.