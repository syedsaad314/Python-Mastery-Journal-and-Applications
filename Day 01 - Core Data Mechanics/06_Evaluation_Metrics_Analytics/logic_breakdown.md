# Logical Breakdown: Evaluation Metrics Analytics

### The Problem
Relying solely on accuracy scores can yield deceptive performance insights when dealing with imbalanced data classes (e.g., medical test results or fraud detection). If a test dataset contains 99% negative cases, a basic model that simply predicts negative every time will achieve 99% accuracy while failing completely as a classifier.

### Architectural Thought Process
I structured the engine to compile a comprehensive base mapping table (TP, FP, TN, FN) in a single loop traversal. The algorithm calculates Precision and Recall using conditional defaults, protecting the system from common runtime calculation issues like division-by-zero errors when handling sparse arrays.

### Complexity & Scope
*   **Time Complexity:** The execution iterates once over the array arrays with a time efficiency of $O(N)$.
*   **AI/ML Real-world Application:** This matrix evaluation methodology forms the standard foundation for calculating performance profiles across classification models, matching tools like Scikit-Learn's `classification_report`.