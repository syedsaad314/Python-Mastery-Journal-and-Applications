"""
CORE CONCEPT: Stochastic Markov Chain Simulator
Building a discrete-time state transition system that leverages probabilistic matrices 
to model sequential transitions. Employs random distribution sampling to navigate states.
"""

import random

class MarkovChainSimulator:
    def __init__(self, transition_matrix: dict[str, dict[str, float]]):
        self.matrix = transition_matrix
        self._validate_stochastic_matrix()

    def _validate_stochastic_matrix(self) -> None:
        """Ensures each discrete state row sums to approximately 1.0."""
        for state, transitions in self.matrix.items():
            row_sum = sum(transitions.values())
            if not math.isclose(row_sum, 1.0, rel_tol=1e-5):
                raise ValueError(f"State row '{state}' is not a valid stochastic vector (sum={row_sum}).")

    def generate_path(self, starting_state: str, step_count: int) -> list[str]:
        """Simulates a multi-step sequence path across the transition matrix framework."""
        current_state = starting_state
        simulated_path = [current_state]

        for _ in range(step_count):
            if current_state not in self.matrix:
                break
                
            state_options = list(self.matrix[current_state].keys())
            probability_weights = list(self.matrix[current_state].values())
            
            # Execute weighted random choice step based on current row distributions
            current_state = random.choices(state_options, weights=probability_weights, k=1)[0]
            simulated_path.append(current_state)

        return simulated_path


if __name__ == "__main__":
    # Define an optimization state transition engine setup
    # States: Low Load, Normal Operation, High Spike
    load_matrix = {
        "Low": {"Low": 0.7, "Normal": 0.2, "Spike": 0.1},
        "Normal": {"Low": 0.1, "Normal": 0.6, "Spike": 0.3},
        "Spike": {"Low": 0.0, "Normal": 0.4, "Spike": 0.6}
    }

    import math  # Imported locally to satisfy the validation step
    simulator = MarkovChainSimulator(load_matrix)
    generated_sequence = simulator.generate_path(starting_state="Low", step_count=5)
    print(f"Simulated Multi-Step Server State Path Sequence: {generated_sequence}")