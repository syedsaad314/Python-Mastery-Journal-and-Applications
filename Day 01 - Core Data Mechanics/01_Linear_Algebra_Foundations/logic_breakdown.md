# Logical Breakdown: Linear Algebra Foundations

### The Problem
In Machine Learning and deep learning frameworks, calculations rely on dot products and matrix transformations. Using pre-built tools abstract away how calculations traverse memory and dimensions. The goal is to build an explicit vector and matrix transformation engine from scratch using core Python lists.

### Architectural Thought Process
1.  **Validation First:** Multiplications fail if dimensions conflict. I designed strict conditional boundaries to capture size mismatches immediately before running calculations.
2.  **Column Reconstruction:** Python stores nested arrays as row-major blocks. To run an efficient dot product across matrices, the inner loops extract columns from the second matrix sequentially to mimic linear transformations natively.

### Complexity & Scope
*   **Time Complexity:** Vector dot product scales linearly at $O(N)$. Matrix multiplication scales cubically at $O(I \times J \times K)$ due to the triple nested loop tracking rows and columns.
*   **AI/ML Real-world Application:** This mirrors exactly how a linear layer passes signals down a neural network model ($Y = WX + B$).