# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Q-Learning Temporal Difference (TD) Update
Description: Executes a model-free learning update rule to shift Q-values 
             towards the expected optimal reward without requiring environment transition maps.
"""
import numpy as np  # type: ignore


class QLearningEngine:
    @staticmethod
    def compute_td_update(Q_table: np.ndarray, state: int, action: int, reward: float, 
                          next_state: int, alpha: float, gamma: float) -> np.ndarray:
        
        # 1. Current Estimate
        current_q = Q_table[state, action]
        
        # 2. Maximum expected future reward from the new state (Greedy policy assumption)
        max_future_q = np.max(Q_table[next_state])
        
        # 3. Temporal Difference (TD) Target
        td_target = reward + (gamma * max_future_q)
        
        # 4. TD Error (Difference between expectation and reality)
        td_error = td_target - current_q
        
        # 5. Update Q-Table in-place via Learning Rate (Alpha)
        Q_table[state, action] = current_q + (alpha * td_error)
        
        return Q_table


if __name__ == "__main__":
    # Initialize a blank Q-Table (3 states, 2 actions)
    q_matrix = np.zeros((3, 2), dtype=np.float64)
    
    # Agent takes Action 1 from State 0, arrives at State 1, receives Reward +10
    updated_q = QLearningEngine.compute_td_update(
        Q_table=q_matrix, state=0, action=1, reward=10.0, next_state=1, alpha=0.1, gamma=0.9
    )
    
    # 0.0 + 0.1 * (10.0 + 0.9*(0.0) - 0.0) = 1.0
    assert updated_q[0, 1] == 1.0
    # Rest of the table should remain untouched (0.0)
    assert np.sum(updated_q) == 1.0 
    
    print(f"[TASK 02 PASSED] Q-Learning TD update executed accurately. New Q-Value: {updated_q[0, 1]:.2f}")