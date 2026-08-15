# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Diffusion Reverse Step (Langevin Dynamics)
Description: Executes a single mathematical backward step (t -> t-1),
             removing predicted Gaussian noise from an image array.
"""
import numpy as np  # type: ignore


class DiffusionReverseEngine:
    def __init__(self, timesteps: int = 1000):
        self.betas = np.linspace(0.0001, 0.02, timesteps)
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = np.cumprod(self.alphas)

    def p_sample_step(self, x_t: np.ndarray, predicted_noise: np.ndarray, t: int) -> np.ndarray:
        # Prevents negative or zero division on the final step
        if t == 0:
            z = np.zeros_like(x_t)
        else:
            z = np.random.standard_normal(size=x_t.shape)
            
        beta_t = self.betas[t]
        alpha_t = self.alphas[t]
        alpha_bar_t = self.alphas_cumprod[t]
        
        # Scaling factor: (1 - alpha_t) / sqrt(1 - alpha_bar_t)
        noise_scaler = (1.0 - alpha_t) / np.sqrt(1.0 - alpha_bar_t)
        
        # Calculate predicted mean (mu_theta)
        # mu = (1 / sqrt(alpha_t)) * (x_t - noise_scaler * predicted_noise)
        mu_theta = (1.0 / np.sqrt(alpha_t)) * (x_t - (noise_scaler * predicted_noise))
        
        # Add variance back (Langevin dynamics stochasticity) unless it's step 0
        sigma_t = np.sqrt(beta_t)
        x_t_minus_1 = mu_theta + (sigma_t * z)
        
        return x_t_minus_1


if __name__ == "__main__":
    np.random.seed(99)
    engine = DiffusionReverseEngine()
    
    # Highly noisy image at t=500
    x_t = np.random.randn(1, 3, 3)
    
    # Model's mathematical prediction of what the exact noise is
    model_predicted_eps = np.random.randn(1, 3, 3) * 0.5
    
    # Execute one reverse denoising step
    x_prev = engine.p_sample_step(x_t, model_predicted_eps, t=500)
    
    assert x_prev.shape == x_t.shape
    assert not np.array_equal(x_t, x_prev)
    
    print(f"[TASK 05 PASSED] Reverse diffusion denoising step executed. Transitioned from t=500 to t=499.")