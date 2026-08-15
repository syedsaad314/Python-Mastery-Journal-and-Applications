# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Diffusion Process - Forward Noise Injection
Description: Computes closed-form Markov chain Gaussian noise injection for 
             arbitrary timestep `t` using variance scheduling.
"""
import numpy as np  # type: ignore


class DiffusionForwardEngine:
    def __init__(self, timesteps: int = 1000):
        # Create a linear variance schedule (beta) from 0.0001 to 0.02
        self.betas = np.linspace(0.0001, 0.02, timesteps)
        
        # Alphas = 1 - betas
        self.alphas = 1.0 - self.betas
        
        # Cumulative product of alphas (alpha_bar) for closed-form sampling
        self.alphas_cumprod = np.cumprod(self.alphas)

    def q_sample_closed_form(self, x_0: np.ndarray, t: int) -> tuple[np.ndarray, np.ndarray]:
        # Returns the noisy image at step t without iterative loops
        alpha_bar_t = self.alphas_cumprod[t]
        
        # Sample random normal noise
        noise = np.random.standard_normal(size=x_0.shape)
        
        # Formula: x_t = sqrt(alpha_bar) * x_0 + sqrt(1 - alpha_bar) * noise
        mean_scale = np.sqrt(alpha_bar_t)
        variance_scale = np.sqrt(1.0 - alpha_bar_t)
        
        x_t = (mean_scale * x_0) + (variance_scale * noise)
        return x_t, noise


if __name__ == "__main__":
    np.random.seed(42)
    engine = DiffusionForwardEngine(timesteps=1000)
    
    # Original pure image matrix (values between -1 and 1)
    x_start = np.ones((1, 3, 3))
    
    # Sample at early timestep t=10 (Minor noise)
    x_t10, n10 = engine.q_sample_closed_form(x_start, t=10)
    
    # Sample at deep timestep t=900 (Heavy noise)
    x_t900, n900 = engine.q_sample_closed_form(x_start, t=900)
    
    # Variance (noise) at t=900 should be significantly higher, obliterating the original image
    assert np.var(x_t900) > np.var(x_t10)
    
    print(f"[TASK 04 PASSED] Closed-form Markov Diffusion Noise applied. Mean at T=900: {np.mean(x_t900):.4f}")