# Logic Breakdown: Learning Rate Schedulers
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
A constant learning rate creates a paradox: if it is too high, the model overshoots the minimum loss threshold and bounces wildly. If it is too low, the model takes thousands of epochs to converge and gets easily stuck in local minima.

## My Approach
I implemented mathematical decay schedules (Exponential and Time-Based Decay). These schedulers act as dynamic throttles. During the first few epochs, the rate remains high, allowing the optimizer to traverse massive loss topologies. As the epochs increment, the learning rate drops exponentially, shifting the optimizer into a fine-grained, micro-adjustment tuning mode to nestle cleanly into the global minimum.

## Complexity Profile
* Runtime Bounds: $O(1)$ arithmetic floating point decay operation per epoch.
* Space Constraints: $O(1)$ static memory bounds.