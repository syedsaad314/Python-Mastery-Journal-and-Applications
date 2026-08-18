# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: PageRank (Eigenvector Centrality)
Description: Evaluates the recursive global importance of graph nodes utilizing the 
             stochastic power iteration method and the teleportation damping factor.
"""
import numpy as np  # type: ignore


class PageRankEngine:
    @staticmethod
    def compute_pagerank(A: np.ndarray, d: float = 0.85, max_iters: int = 100, tol: float = 1e-6) -> np.ndarray:
        N = A.shape[0]
        
        # 1. Construct Column-Stochastic Transition Matrix (M)
        # Out-degrees (sum of columns)
        out_degrees = np.sum(A, axis=0)
        out_degrees[out_degrees == 0] = 1.0  # Prevent division by zero for sink nodes
        
        M = A / out_degrees
        
        # 2. Initialize PageRank vector uniformly
        v = np.ones(N) / N
        
        # 3. Power Iteration to find principal eigenvector
        for _ in range(max_iters):
            v_prev = np.copy(v)
            
            # PR Formula: v = (1 - d)/N + d * M * v
            v = ((1.0 - d) / N) + (d * np.dot(M, v_prev))
            
            # Check for mathematical convergence (L1 Norm)
            if np.sum(np.abs(v - v_prev)) < tol:
                break
                
        return v


if __name__ == "__main__":
    # Directed Graph: 0->1, 0->2, 1->2, 2->0
    A_web = np.array([
        [0, 0, 1], # Node 2 links to 0
        [1, 0, 0], # Node 0 links to 1
        [1, 1, 0]  # Node 0 and 1 link to 2
    ], dtype=np.float64)
    
    pr_scores = PageRankEngine.compute_pagerank(A_web, d=0.85)
    
    assert pr_scores.shape == (3,)
    # Probabilities must sum to 1.0
    assert abs(np.sum(pr_scores) - 1.0) < 1e-6
    
    # Node 2 receives links from both 0 and 1, making it the most "central/important" node
    assert pr_scores[2] > pr_scores[0]
    assert pr_scores[2] > pr_scores[1]
    
    print(f"[TASK 06 PASSED] PageRank Centrality resolved. Scores converged to: {pr_scores}")