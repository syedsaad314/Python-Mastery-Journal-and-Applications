# Portfolio Code Review: High-Performance Single-Threaded Asynchronous Static File Server
**Author:** Syed Saad Bin Irfan

## Practical Context
This server replicates the non-blocking architecture used by production engines like Nginx, handling heavy static file delivery workloads on a single thread without incurring high multi-threading context-switching overhead.

## Engineering Standards Applied
* **Stateful Flow Segregation:** Decouples heavy file read/write operations by updating socket registration masks dynamically (`selectors.EVENT_WRITE`), ensuring the server handles data transfers without blocking the main event loop.
* **Controlled Streaming Windows:** Streams data in structured 4KB chunks based on socket availability. This prevents slow network consumers from bottlenecking system memory or stalling the event processing path.
* **Proactive Resource Recovery:** Cleans up file descriptors and updates selector registration paths automatically during client disconnections or transmission errors, preventing resource leak issues.