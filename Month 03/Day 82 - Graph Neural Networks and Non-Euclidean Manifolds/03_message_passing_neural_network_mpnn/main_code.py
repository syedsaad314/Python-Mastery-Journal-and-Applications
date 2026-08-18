# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Spatial Message Passing Neural Network (MPNN)
Description: Decouples the graph operation into distinct 'Aggregate' and 'Update' 
             spatial phases, allowing non-linear transformations on the edge messages.
"""
import numpy as np  # type: ignore


class MessagePassingEngine:
    @staticmethod
    def spatial_aggregate_and_update(A: np.ndarray, X: np.ndarray, W_msg: np.ndarray, W_update: np.ndarray) -> np.ndarray:
        num_nodes = A.shape[0]
        feature_dim = X.shape[1]
        
        # 1. MESSAGE PHASE: Transform raw node features into 'Messages'
        # M = X * W_msg
        messages = np.dot(X, W_msg)
        
        # 2. AGGREGATE PHASE: Nodes sum the messages from their physical neighbors
        # A * M explicitly restricts data flow to established graph edges
        aggregated_messages = np.dot(A, messages)
        
        # 3. UPDATE PHASE: Combine the node's own original features with aggregated neighbor data
        # H_new = ReLU( Concat(X, Agg_M) * W_update )
        concat_state = np.hstack((X, aggregated_messages))
        new_state = np.maximum(0, np.dot(concat_state, W_update))
        
        return new_state


if __name__ == "__main__":
    np.random.seed(99)
    # 4 Nodes. Directed graph: 0->1, 1->2, 2->3
    A_directed = np.array([
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ], dtype=np.float64)
    
    # Node features (4 nodes, 2 features)
    X_nodes = np.random.randn(4, 2)
    
    # Message transform weights (2 -> 3 dimensions)
    W_m = np.random.randn(2, 3)
    
    # Update transform weights (Concat(2 + 3) -> 4 dimensions)
    W_u = np.random.randn(5, 4)
    
    updated_nodes = MessagePassingEngine.spatial_aggregate_and_update(A_directed, X_nodes, W_m, W_u)
    
    assert updated_nodes.shape == (4, 4)
    
    # Node 0 has no incoming edges, so its aggregated message vector is strictly zeros
    assert np.allclose(np.dot(A_directed[0], np.dot(X_nodes, W_m)), np.zeros(3))
    
    print(f"[TASK 03 PASSED] Spatial Message Passing executed. Forward states aggregated via adjacency paths.")