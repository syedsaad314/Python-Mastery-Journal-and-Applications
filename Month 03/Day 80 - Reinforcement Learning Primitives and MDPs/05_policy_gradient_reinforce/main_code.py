# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: REINFORCE Policy Gradient Primitive
Description: Computes the loss required to push the network to increase the probability 
             of actions that led to high cumulative rewards using the Log-Derivative trick.
"""
import numpy as np  # type: ignore


class PolicyGradientEngine:
    @staticmethod
    def compute_policy_loss(action_probabilities: np.ndarray, 
                            action_taken_indices: np.ndarray, 
                            discounted_rewards: np.ndarray) -> float:
        
        # 1. Isolate the probability the neural network assigned to the action actually taken
        # Advanced indexing: grabs the probability for each step
        batch_size = len(action_taken_indices)
        probs_of_actions_taken = action_probabilities[np.arange(batch_size), action_taken_indices]
        
        # 2. Prevent log(0) numeric crash
        eps = 1e-12
        log_probs = np.log(probs_of_actions_taken + eps)
        
        # 3. Objective: Maximize E[log(pi) * G_t]
        # Since optimizers MINIMIZE by default, we take the negative mean
        loss = -np.mean(log_probs * discounted_rewards)
        
        return float(loss)


if __name__ == "__main__":
    # 3-step episode. Action space = 2.
    # Network assigned these probabilities to actions [0, 1] during the run
    predicted_probs = np.array([
        [0.2, 0.8],  # Step 0
        [0.6, 0.4],  # Step 1
        [0.9, 0.1]   # Step 2
    ])
    
    # The actions the agent actually randomly sampled/took
    actions_taken = np.array([1, 0, 1])
    
    # The discounted rewards evaluated from that trajectory
    G_t = np.array([10.0, 8.0, -5.0]) 
    
    # If reward is positive, network is penalized for low probability. 
    # If reward is negative, network is rewarded for low probability.
    pg_loss = PolicyGradientEngine.compute_policy_loss(predicted_probs, actions_taken, G_t)
    
    assert pg_loss is not None
    # Action 2 (idx=1) had -5 reward and 0.1 prob. Network was "right" to give it low prob.
    
    print(f"[TASK 05 PASSED] REINFORCE Policy Gradient loss computed. Scalar Loss: {pg_loss:.4f}")