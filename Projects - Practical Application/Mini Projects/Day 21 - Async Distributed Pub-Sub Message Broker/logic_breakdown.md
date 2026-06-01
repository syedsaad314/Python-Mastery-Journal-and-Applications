# Portfolio Code Review: Distributed Async Pub-Sub Message Broker
**Engineer:** Syed Saad Bin Irfan

## The Problem
Synchronous message routing patterns choke when handling high-volume cross-client broadcasts. Traditional models create processing bottlenecks where slow networks drop connection updates and stall overall system message distribution.

## Engineering Standards Applied
* **Custom Segmented Protocol Parsing:** Implements a fast, line-based network protocol (`SUB:<topic>` and `PUB:<topic>:<payload>`). This custom design avoids heavy JSON parsing overhead, allowing single-threaded socket frames to process quickly.
* **Automated Subscription Leaks Cleanup:** Uses structured `finally` blocks to intercept socket disconnections. The system automatically unregisters the dead client from all active topic maps, preventing memory leaks and resource starvation.
* **Isolated Outbound Error Buffering:** Wraps outbound operations in targeted `try/except` loops, ensuring that individual socket failures or client drops do not disrupt or delay sibling deliveries.