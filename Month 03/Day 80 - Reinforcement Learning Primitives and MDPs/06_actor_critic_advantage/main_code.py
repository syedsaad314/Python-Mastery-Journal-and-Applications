# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Advantage Calculation (Actor-Critic)
Description: Stabilizes high-variance policy gradients by establishing a baseline 
             Critic (V), scaling updates relative to how much better an action was than expected.
"""
import numpy as np  # type: ignore


class AdvantageFunctionEngine:
    @staticmethod
    def compute_advantage(rewards: np.ndarray, values: np.ndarray, gamma: float = 0.99) -> np.ndarray:
        # Validate shapes: values contains an extra element V(s_T+1) representing terminal state
        T = len(rewards)
        if len(values) != T + 1:
            raise ValueError("Value array must be length T+1 to calculate terminal boundary.")
            
        advantages = np.zeros(T, dtype=np.float64)
        
        # Advantage A_t = R_t + gamma * V(s_t+1) - V(s_t)
        # This is essentially the 1-step Temporal Difference Error (TD-Error)
        for t in range(T):
            td_target = rewards[t] + (gamma * values[t+1])
            advantages[t] = td_target - values[t]
            
        return advantages


if __name__ == "__main__":
    # T=3 Steps
    seq_rewards = np.array([1.0, 1.0, 10.0])
    
    # Critic's Value predictions for the states [t=0, t=1, t=2, terminal]
    # At t=2, Critic expected 5.0. It actually received 10.0
    critic_values = np.array([2.0, 3.0, 5.0, 0.0])
    
    advantage_vector = AdvantageFunctionEngine.compute_advantage(seq_rewards, critic_values, gamma=1.0)
    
    assert advantage_vector.shape == (3,)
    # A_2 = R_2 + 1.0*V_term - V_2 = 10.0 + 0 - 5.0 = 5.0
    assert advantage_vector[2] == 5.0
    # A_0 = 1.0 + 3.0 - 2.0 = 2.0
    assert advantage_vector[0] == 2.0
    
    print(f"[TASK 06 PASSED] Actor-Critic Advantage resolved. Trajectory Advantages: {advantage_vector}")