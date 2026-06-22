# Logical Breakdown: Binary Decision Tree Split Router

### The Problem
Machine learning classifiers like Random Forests and XGBoost output predictions by processing data matrices through nested logic gates. Simply nesting hardcoded `if-else` loops creates rigid systems that cannot change dynamically. We need a flexible, memory-linked tree node architecture that reads and evaluates configurations at runtime.

### Architectural Thought Process
I structured the decision logic using an object-oriented composite pattern. Each `DecisionNode` functions as either a routing rule or a terminal value (leaf node). Non-terminal nodes contain a target data feature index and a mathematical cutoff value. By separating data routing logic from structural values, the engine can traverse complex branches dynamically using recursive memory pointers.

### Complexity & Scope
*   **Time Complexity:** Evaluation scans operate at a scale of $O(D)$, where $D$ represents the depth trajectory from root to leaf. For balanced layouts, this guarantees sub-linear runtime scaled at $O(\log N)$.
*   **AI/ML Real-world Application:** This architecture provides the foundational model pattern for implementing Decision Trees from scratch, matching libraries like Scikit-Learn's `DecisionTreeClassifier`.