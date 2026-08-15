# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Epsilon-Greedy Exploration Policy with Decay
Description: Balances exploration of unknown states against exploitation of known 
             rewards using an exponentially decaying epsilon threshold.
"""
import numpy as np  # type: ignore


class ExplorationPolicyEngine:
    @staticmethod
    def select_action(q_values_for_state: np.ndarray, epsilon: float) -> int:
        rng = np.random.default_rng()
        
        # Generate random float [0.0, 1.0)
        if rng.random() < epsilon:
            # EXPLORE: Pick a random action uniformly
            return int(rng.integers(0, len(q_values_for_state)))
        else:
            # EXPLOIT: Pick the action with the highest Q-value
            # If there's a tie, argmax naturally picks the first index
            return int(np.argmax(q_values_for_state))

    @staticmethod
    def decay_epsilon(current_epsilon: float, decay_rate: float, min_epsilon: float = 0.01) -> float:
        # Exponential decay formula
        new_epsilon = current_epsilon * decay_rate
        return max(new_epsilon, min_epsilon)


if __name__ == "__main__":
    q_state = np.array([0.1, 5.0, 0.2, -1.0])
    
    # 1. Full Exploitation Test (Epsilon = 0.0)
    action_exploit = ExplorationPolicyEngine.select_action(q_state, epsilon=0.0)
    assert action_exploit == 1  # Index of highest Q-value (5.0)
    
    # 2. Decay Validation
    eps_start = 1.0
    eps_decayed = ExplorationPolicyEngine.decay_epsilon(eps_start, decay_rate=0.9)
    assert eps_decayed == 0.9
    
    # 3. Floor validation
    eps_floor = ExplorationPolicyEngine.decay_epsilon(0.015, decay_rate=0.1, min_epsilon=0.01)
    assert eps_floor == 0.01
    
    print(f"[TASK 03 PASSED] Epsilon-Greedy logic functional. Exploitation defaults to Action {action_exploit}.")