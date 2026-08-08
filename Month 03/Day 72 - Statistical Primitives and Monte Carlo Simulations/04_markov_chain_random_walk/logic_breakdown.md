# Logic Breakdown: Markov Chain State Transitions
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Predicting sequential, memoryless stochastic events iteratively step-by-step ($X_1 \rightarrow X_2 \dots \rightarrow X_N$) using sequential probability loops is slow and mathematically clumsy.

## My Approach
I modeled the system as a Markov Chain. Because the process fulfills the Markov property (the next state depends *only* on the current state), the entire sequence of probabilities over $N$ steps mathematically collapses into a single matrix exponentiation operation: $S_n = S_0 \cdot P^n$. Using `np.linalg.matrix_power`, the engine bypasses sequential loops and calculates powers via optimized binary exponentiation ($O(\log N)$ multiplications).

## Complexity Profile
* Runtime Bounds: $O(K^3 \log N)$ where $K$ is the matrix dimension (number of states) and $N$ is the number of steps.
* Space Constraints: $O(K^2)$ auxiliary allocation bounded by the transition matrix dimensions.