"""
CORE CONCEPT: Viterbi Sequential Decoding Engine
Implementing a dynamic programming algorithm over a Hidden Markov Model (HMM).
Determines the most likely sequence of hidden states that produced a given 
series of observed data points.
"""

class ViterbiDecodingEngine:
    @staticmethod
    def decode_hidden_sequence(
        observations: list[str],
        states: list[str],
        start_prob: dict[str, float],
        trans_prob: dict[str, dict[str, float]],
        emit_prob: dict[str, dict[str, float]]
    ) -> list[str]:
        """Calculates the most probable hidden state sequence using dynamic programming."""
        # viterbi_matrix[step][state] = highest probability value tracking
        viterbi_matrix = [{}]
        path_tracker = {}

        # Step 0: Initialize tracking matrix paths using base start probabilities
        for state in states:
            viterbi_matrix[0][state] = start_prob[state] * emit_prob[state].get(observations[0], 0.0)
            path_tracker[state] = [state]

        # Process the remaining observation sequence steps sequentially
        for t in range(1, len(observations)):
            viterbi_matrix.append({})
            new_path_tracker = {}

            for current_state in states:
                # Find maximum probability step transition coming from previous state choices
                (prob, best_prior_state) = max(
                    (viterbi_matrix[t-1][prior_state] * trans_prob[prior_state].get(current_state, 0.0), prior_state)
                    for prior_state in states
                )
                
                # Calculate total probability including the current observation emission
                total_calculated_prob = prob * emit_prob[current_state].get(observations[t], 0.0)
                viterbi_matrix[t][current_state] = total_calculated_prob
                
                # Update optimal sequence paths
                new_path_tracker[current_state] = path_tracker[best_prior_state] + [current_state]

            path_tracker = new_path_tracker

        # Locate final argmax state termination sequence path point
        (_, terminal_state) = max((viterbi_matrix[-1][state], state) for state in states)
        return path_tracker[terminal_state]


if __name__ == "__main__":
    # Setup HMM dimensions: Hidden states represent underlying weather; observations represent item choices
    hidden_states = ["Sunny", "Rainy"]
    observation_sequence = ["Umbrella", "T-Shirt", "Umbrella"]

    start_probabilities = {"Sunny": 0.6, "Rainy": 0.4}
    transition_probabilities = {
        "Sunny": {"Sunny": 0.7, "Rainy": 0.3},
        "Rainy": {"Sunny": 0.4, "Rainy": 0.6}
    }
    emission_probabilities = {
        "Sunny": {"T-Shirt": 0.8, "Umbrella": 0.2},
        "Rainy": {"T-Shirt": 0.1, "Umbrella": 0.9}
    }

    decoder = ViterbiDecodingEngine()
    resolved_sequence = decoder.decode_hidden_sequence(
        observation_sequence, hidden_states, start_probabilities, transition_probabilities, emission_probabilities
    )
    print(f"Most Likely Decoded Hidden State Sequence Path: {resolved_sequence}")