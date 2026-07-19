# Logic Breakdown: Fault Injection Resilience Matrix
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
You can't prove a distributed architecture is resilient just by testing the happy path. If you wait for actual production network crashes to find out if your compensation rollbacks work, you risk data corruption when a real failure happens.

## My Approach
I built a dedicated fault-injection framework. It intentionally injects infrastructure crashes, network cuts, and timeout flags into the running transaction loop, verifying that the system catches errors reliably and executes its cleanup routines perfectly.

## Complexity Profile
* Runtime Bounds: Intercepting errors and running compensation code finishes in constant O(1) time.
* Space Constraints: Operates efficiently inside a fixed, minimal memory profile of O(1).