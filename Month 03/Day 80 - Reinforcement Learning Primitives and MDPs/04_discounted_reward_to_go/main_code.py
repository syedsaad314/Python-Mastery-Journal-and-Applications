# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Discounted Returns (Reward-to-Go)
Description: Calculates the cumulative discounted return for an entire episode 
             backwards to evaluate temporal action effectiveness in Policy Gradients.
"""
import numpy as np  # type: ignore


class DiscountedReturnEngine:
    @staticmethod
    def calculate_rewards_to_go(rewards_sequence: list[float], gamma: float = 0.99) -> np.ndarray:
        # Number of steps in the episode
        T = len(rewards_sequence)
        discounted_returns = np.zeros(T, dtype=np.float64)
        
        running_add = 0.0
        
        # Calculate backwards: G_t = R_t + gamma * G_{t+1}
        for t in reversed(range(T)):
            running_add = rewards_sequence[t] + (gamma * running_add)
            discounted_returns[t] = running_add
            
        return discounted_returns


if __name__ == "__main__":
    # Agent survives for 4 steps, then fails (Reward: 0, 0, 0, 10)
    episode_rewards = [0.0, 0.0, 0.0, 10.0]
    gamma_val = 0.9
    
    returns = DiscountedReturnEngine.calculate_rewards_to_go(episode_rewards, gamma=gamma_val)
    
    # Assert backwards propagation of delayed rewards
    # G_3 = 10.0
    assert returns[3] == 10.0
    # G_2 = 0 + 0.9(10) = 9.0
    assert returns[2] == 9.0
    # G_1 = 0 + 0.9(9) = 8.1
    assert abs(returns[1] - 8.1) < 1e-6
    # G_0 = 0 + 0.9(8.1) = 7.29
    assert abs(returns[0] - 7.29) < 1e-6
    
    print(f"[TASK 04 PASSED] Rewards-to-go computed backward. Value at T=0: {returns[0]:.4f}")