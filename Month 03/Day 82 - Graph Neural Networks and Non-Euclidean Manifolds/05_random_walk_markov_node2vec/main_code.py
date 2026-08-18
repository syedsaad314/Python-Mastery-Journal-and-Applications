# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Graph Random Walks (Node2Vec Primitive)
Description: Simulates stochastic Markov transitions across a graph topology to extract 
             sequential node contexts, bridging graph structures into Word2Vec NLP logic.
"""
import numpy as np  # type: ignore


class RandomWalkEngine:
    @staticmethod
    def generate_transition_matrix(A: np.ndarray) -> np.ndarray:
        # Create Markov Transition Matrix (Rows sum to 1.0)
        degrees = np.sum(A, axis=1)
        # Avoid division by zero for isolated nodes
        degrees[degrees == 0] = 1.0 
        
        # P_ij = A_ij / Degree_i
        P_transition = A / degrees[:, np.newaxis]
        return P_transition

    @staticmethod
    def simulate_walk(P: np.ndarray, start_node: int, walk_length: int) -> list[int]:
        rng = np.random.default_rng()
        num_nodes = P.shape[0]
        
        walk = [start_node]
        current_node = start_node
        
        for _ in range(walk_length - 1):
            probabilities = P[current_node]
            # Randomly select the next node based on edge probabilities
            next_node = rng.choice(np.arange(num_nodes), p=probabilities)
            walk.append(next_node)
            current_node = next_node
            
        return walk


if __name__ == "__main__":
    # Complete Bipartite-like dense graph setup
    A_network = np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ], dtype=np.float64)
    
    P_matrix = RandomWalkEngine.generate_transition_matrix(A_network)
    
    # Assert row probabilities sum to 1.0
    assert np.allclose(np.sum(P_matrix, axis=1), 1.0)
    
    # Node 0 has 2 edges, probability of picking either should be 0.5
    assert P_matrix[0, 1] == 0.5
    
    # Generate a walk of length 10 starting at Node 0
    sampled_walk = RandomWalkEngine.simulate_walk(P_matrix, start_node=0, walk_length=10)
    
    assert len(sampled_walk) == 10
    assert sampled_walk[0] == 0
    
    print(f"[TASK 05 PASSED] Random Walk successfully navigated Markov transition grid: {sampled_walk}")