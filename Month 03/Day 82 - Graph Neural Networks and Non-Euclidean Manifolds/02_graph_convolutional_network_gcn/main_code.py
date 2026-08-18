# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Spectral Graph Convolutional Network (GCN) Propagation
Description: Executes Kipf & Welling's localized first-order spectral approximation, 
             passing node features through normalized adjacency matrices.
"""
import numpy as np  # type: ignore


class GCNPropagationEngine:
    @staticmethod
    def gcn_layer_forward(A: np.ndarray, X: np.ndarray, W: np.ndarray) -> np.ndarray:
        # 1. Add Self-Loops: A_hat = A + I
        # Prevents nodes from ignoring their own features during aggregation
        I = np.eye(A.shape[0])
        A_hat = A + I
        
        # 2. Compute Degree Matrix of A_hat
        D_hat = np.diag(np.sum(A_hat, axis=1))
        
        # 3. Compute D_hat^{-1/2} for symmetric normalization
        # D_hat is diagonal, so we just take the inverse square root of the diagonal elements
        D_hat_inv_sqrt = np.diag(1.0 / np.sqrt(np.diag(D_hat)))
        
        # 4. Symmetric Normalized Adjacency: D_hat^{-1/2} * A_hat * D_hat^{-1/2}
        A_norm = np.dot(D_hat_inv_sqrt, np.dot(A_hat, D_hat_inv_sqrt))
        
        # 5. GCN Forward Pass: Z = ReLU(A_norm * X * W)
        # Message passing + Linear Transformation
        node_embeddings = np.dot(A_norm, np.dot(X, W))
        H_next = np.maximum(0, node_embeddings)  # ReLU
        
        return H_next


if __name__ == "__main__":
    np.random.seed(42)
    # 3 Nodes, connected in a line (0-1-2)
    A_graph = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ], dtype=np.float64)
    
    # 3 Nodes, 2 Features per node
    X_features = np.array([
        [1.0, -1.0],
        [2.0, -2.0],
        [3.0, -3.0]
    ], dtype=np.float64)
    
    # Weights projecting 2 features to 4 hidden features
    W_layer = np.random.randn(2, 4)
    
    H_out = GCNPropagationEngine.gcn_layer_forward(A_graph, X_features, W_layer)
    
    assert H_out.shape == (3, 4)
    assert np.all(H_out >= 0.0)  # ReLU ensures non-negativity
    
    print(f"[TASK 02 PASSED] GCN Spectral Convolution executed. Output Node Embeddings Shape: {H_out.shape}")