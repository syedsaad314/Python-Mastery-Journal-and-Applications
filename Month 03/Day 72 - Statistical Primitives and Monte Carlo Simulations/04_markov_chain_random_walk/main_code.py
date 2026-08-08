# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Markov Chain State Transitions
Description: Uses linear algebra and matrix exponentiation to predict 
             stochastic state transition distributions over N steps.
"""
import numpy as np  # type: ignore


class MarkovChainEngine:
    @staticmethod
    def predict_state_distribution(transition_matrix: np.ndarray, initial_state: np.ndarray, steps: int) -> np.ndarray:
        # Validate probability rules: Rows must sum to 1
        if not np.allclose(np.sum(transition_matrix, axis=1), 1.0):
            raise ValueError("Transition matrix rows must sum to 1 (valid probabilities).")
            
        # P^n gives the transition probabilities after 'steps' transitions
        # np.linalg.matrix_power optimizes repetitive matrix multiplication via binary exponentiation
        n_step_transition = np.linalg.matrix_power(transition_matrix, steps)
        
        # State_n = Initial_State * P^n
        future_state = np.dot(initial_state, n_step_transition)
        return future_state


if __name__ == "__main__":
    # States: [Sunny, Rainy]
    # Sunny -> Sunny (0.8), Sunny -> Rainy (0.2)
    # Rainy -> Sunny (0.4), Rainy -> Rainy (0.6)
    P_matrix = np.array([
        [0.8, 0.2],
        [0.4, 0.6]
    ], dtype=np.float64)
    
    # We are 100% starting on a Sunny day
    current_weather = np.array([1.0, 0.0], dtype=np.float64)
    
    # Predict weather probability 10 days from now
    state_day_10 = MarkovChainEngine.predict_state_distribution(P_matrix, current_weather, steps=10)
    
    assert state_day_10.shape == (2,)
    assert abs(np.sum(state_day_10) - 1.0) < 1e-9
    
    print(f"[TASK 04 PASSED] Markov Chain predicted state after 10 days. Sunny: {state_day_10[0]:.2%}, Rainy: {state_day_10[1]:.2%}")