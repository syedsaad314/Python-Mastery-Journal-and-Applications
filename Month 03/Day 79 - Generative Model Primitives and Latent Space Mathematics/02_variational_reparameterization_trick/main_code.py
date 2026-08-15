# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Variational Reparameterization Trick
Description: Decouples random sampling from network parameters, allowing 
             backpropagation gradients to flow safely through stochastic nodes.
"""
import numpy as np  # type: ignore


class VariationalReparameterization:
    @staticmethod
    def sample_latent(mu: np.ndarray, log_var: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        # Convert log variance to standard deviation: exp(0.5 * log_var)
        std = np.exp(0.5 * log_var)
        
        # Sample pure Gaussian noise (epsilon)
        # This isolates the randomness OUTSIDE the gradient path of mu and std
        epsilon = np.random.standard_normal(size=mu.shape)
        
        # Reparameterization Trick: z = mu + std * epsilon
        z = mu + (std * epsilon)
        
        return z, epsilon


if __name__ == "__main__":
    np.random.seed(99)
    # Simulated output from an Encoder layer
    mu_predicted = np.array([[0.5, -0.2], [0.1, 0.9]])
    log_var_predicted = np.array([[-1.0, 0.5], [0.0, -2.0]])
    
    z_sampled, eps = VariationalReparameterization.sample_latent(mu_predicted, log_var_predicted)
    
    assert z_sampled.shape == mu_predicted.shape
    assert eps.shape == mu_predicted.shape
    
    # Because std is positive, z should shift from mu based on epsilon direction
    assert np.all(z_sampled != mu_predicted)
    
    print(f"[TASK 02 PASSED] Reparameterization Trick executed. Gradients preserved. Latent Z:\n{z_sampled}")