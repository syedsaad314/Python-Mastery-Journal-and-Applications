# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Graph Representations & The Laplacian Matrix
Description: Computes the Degree Matrix and the Unnormalized Graph Laplacian, 
             the foundational matrix bridging discrete graph topology with continuous calculus.
"""
import numpy as np  # type: ignore
from typing import Tuple


class GraphMatrixEngine:
    @staticmethod
    def compute_laplacian(adjacency_matrix: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        # Validate symmetry for undirected graphs
        if not np.allclose(adjacency_matrix, adjacency_matrix.T):
            raise ValueError("Adjacency matrix must be symmetric for undirected graphs.")
            
        # 1. Degree Matrix (D): Diagonal matrix containing the sum of edges per node
        degrees = np.sum(adjacency_matrix, axis=1)
        D = np.diag(degrees)
        
        # 2. Graph Laplacian (L): D - A
        L = D - adjacency_matrix
        
        return degrees, D, L


if __name__ == "__main__":
    # Undirected Graph with 4 Nodes
    # Node 0 connected to 1, 2
    # Node 1 connected to 0, 2
    # Node 2 connected to 0, 1, 3
    # Node 3 connected to 2
    A = np.array([
        [0, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0]
    ], dtype=np.float64)
    
    degs, D_mat, L_mat = GraphMatrixEngine.compute_laplacian(A)
    
    # Assert degrees: Node 0 has 2 edges, Node 2 has 3 edges
    assert degs[0] == 2.0
    assert degs[2] == 3.0
    
    # Assert Laplacian properties: Rows of L must sum exactly to 0
    row_sums = np.sum(L_mat, axis=1)
    assert np.allclose(row_sums, 0.0)
    
    print(f"[TASK 01 PASSED] Graph Laplacian derived. Laplacian Matrix:\n{L_mat}")