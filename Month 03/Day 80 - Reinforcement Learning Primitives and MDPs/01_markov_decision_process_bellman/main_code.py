# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Bellman Optimality Equation (Value Iteration)
Description: Iteratively calculates the exact optimal state values in a Markov 
             Decision Process (MDP) by projecting future expected rewards.
"""
import numpy as np  # type: ignore


class BellmanEquationEngine:
    @staticmethod
    def value_iteration(P_transitions: np.ndarray, Rewards: np.ndarray, 
                        gamma: float = 0.99, theta: float = 1e-6, max_iters: int = 1000) -> np.ndarray:
        # P_transitions shape: (num_states, num_actions, num_states)
        # Rewards shape: (num_states, num_actions)
        num_states, num_actions, _ = P_transitions.shape
        
        # Initialize Value function for all states to zero
        V = np.zeros(num_states, dtype=np.float64)
        
        for _ in range(max_iters):
            V_prev = np.copy(V)
            
            # Vectorized Bellman Update: V(s) = max_a [ R(s, a) + gamma * sum_{s'} P(s'|s,a) * V(s') ]
            # np.dot(P, V) yields expected future value per state-action pair
            expected_future_value = np.dot(P_transitions, V_prev)
            
            # Action-Value function (Q)
            Q_sa = Rewards + (gamma * expected_future_value)
            
            # Optimal policy takes the max action
            V = np.max(Q_sa, axis=1)
            
            # Convergence check
            if np.max(np.abs(V - V_prev)) < theta:
                break
                
        return V


if __name__ == "__main__":
    # 2 States, 2 Actions
    # P[state, action, next_state]
    P = np.array([
        [[0.8, 0.2], [0.1, 0.9]],  # From State 0 (Action 0 / Action 1)
        [[0.5, 0.5], [1.0, 0.0]]   # From State 1 (Action 0 / Action 1)
    ], dtype=np.float64)
    
    # R[state, action]
    R = np.array([
        [1.0, 0.0],  # State 0 rewards
        [0.0, 5.0]   # State 1 rewards
    ], dtype=np.float64)
    
    optimal_values = BellmanEquationEngine.value_iteration(P, R, gamma=0.9)
    
    assert optimal_values.shape == (2,)
    # State 1 should have a much higher expected value due to the 5.0 reward trap
    assert optimal_values[1] > optimal_values[0]
    
    print(f"[TASK 01 PASSED] Bellman Value Iteration converged. Optimal V: {optimal_values}")