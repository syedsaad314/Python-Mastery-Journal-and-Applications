# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Gaussian Kernel Density Estimation (KDE)
Description: Smooths discrete data points into a continuous probability density curve 
             using vectorized array broadcasting.
"""
import numpy as np  # type: ignore


class KernelDensityEngine:
    @staticmethod
    def estimate_density(data: np.ndarray, x_eval: np.ndarray, bandwidth: float) -> np.ndarray:
        if bandwidth <= 0:
            raise ValueError("Bandwidth smoothing parameter must be positive.")
            
        n_samples = len(data)
        
        # Reshape for broadcasting: x_eval (M, 1) - data (1, N) -> distances matrix (M, N)
        # This calculates the distance of every evaluation point to every data point.
        distances = x_eval[:, np.newaxis] - data[np.newaxis, :]
        
        # Apply Gaussian Kernel: (1/sqrt(2pi)) * exp(-0.5 * (d / h)^2)
        kernels = (1.0 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * np.square(distances / bandwidth))
        
        # Average the kernels across all data points to get the density at each x_eval
        density = np.sum(kernels, axis=1) / (n_samples * bandwidth)
        
        return density


if __name__ == "__main__":
    # 2 discrete data points
    observations = np.array([1.0, 3.0], dtype=np.float64)
    
    # 3 evaluation points
    eval_space = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    
    densities = KernelDensityEngine.estimate_density(observations, eval_space, bandwidth=0.5)
    
    assert densities.shape == (3,)
    # Density at x=1 and x=3 should be symmetric
    assert abs(densities[0] - densities[2]) < 1e-6
    assert densities[0] > 0
    
    print(f"[TASK 02 PASSED] Vectorized KDE computed across evaluation space: {densities}")