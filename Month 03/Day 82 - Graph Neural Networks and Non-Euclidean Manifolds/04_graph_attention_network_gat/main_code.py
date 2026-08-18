# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Graph Attention Network (GAT) Masking
Description: Calculates self-attention weights between nodes, but strictly limits 
             attention scope to physical neighbors using adjacency masking.
"""
import numpy as np  # type: ignore


class GATMaskingEngine:
    @staticmethod
    def compute_masked_attention(X: np.ndarray, A: np.ndarray, W: np.ndarray, a_vec: np.ndarray) -> np.ndarray:
        # 1. Linear Transformation: H = XW
        H = np.dot(X, W)
        
        # 2. Compute attention score for every pair (i, j): LeakyReLU(a^T [Wh_i || Wh_j])
        N = H.shape[0]
        attention_scores = np.zeros((N, N), dtype=np.float64)
        
        for i in range(N):
            for j in range(N):
                # Concatenate node i and node j
                concat_ij = np.concatenate([H[i], H[j]])
                # Apply attention weight vector and LeakyReLU
                score = np.dot(a_vec, concat_ij)
                attention_scores[i, j] = score if score > 0 else 0.01 * score
                
        # 3. Apply Topological Masking
        # If no edge exists in Adjacency matrix (and not a self-loop), set score to -Infinity
        mask = A + np.eye(N)
        masked_scores = np.where(mask > 0, attention_scores, -1e9)
        
        # 4. Softmax across neighbors
        shifted_scores = masked_scores - np.max(masked_scores, axis=1, keepdims=True)
        exp_scores = np.exp(shifted_scores)
        attention_weights = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        
        # 5. Output features = Attention_Weights * H
        H_out = np.dot(attention_weights, H)
        return H_out


if __name__ == "__main__":
    np.random.seed(42)
    # 3 Nodes. 0 connects to 1. 1 connects to 2.
    A_mat = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ], dtype=np.float64)
    
    # 3 nodes, 2 features
    X_mat = np.random.randn(3, 2)
    
    # W transforms 2 features -> 4 features
    W_mat = np.random.randn(2, 4)
    
    # a_vec expects concatenated features: 4 + 4 = 8
    a_weights = np.random.randn(8)
    
    out_features = GATMaskingEngine.compute_masked_attention(X_mat, A_mat, W_mat, a_weights)
    
    assert out_features.shape == (3, 4)
    
    print(f"[TASK 04 PASSED] Graph Attention Network computed masked spatial weights successfully.")