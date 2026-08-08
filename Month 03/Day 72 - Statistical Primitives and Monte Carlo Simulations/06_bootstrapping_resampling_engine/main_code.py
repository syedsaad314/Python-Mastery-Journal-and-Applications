# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Bootstrapping Resampling Engine
Description: Generates empirical sampling distributions via random sampling with 
             replacement, bypassing theoretical assumption requirements.
"""
import numpy as np  # type: ignore


class BootstrappingEngine:
    @staticmethod
    def bootstrap_mean_confidence_interval(data: np.ndarray, num_iterations: int = 1000, alpha: float = 0.05) -> tuple:
        n_samples = len(data)
        rng = np.random.default_rng(42)
        
        # 1. Generate an index matrix of shape (num_iterations, n_samples)
        # Represents drawing indices randomly WITH replacement.
        random_indices = rng.integers(0, n_samples, size=(num_iterations, n_samples))
        
        # 2. Extract bootstrapped datasets using array indexing
        bootstrap_samples = data[random_indices]
        
        # 3. Compute metric of interest (e.g., mean) across axis=1 for all iterations simultaneously
        bootstrap_means = np.mean(bootstrap_samples, axis=1)
        
        # 4. Extract confidence intervals from the empirical percentiles
        lower_percentile = (alpha / 2.0) * 100
        upper_percentile = (1.0 - (alpha / 2.0)) * 100
        
        ci_lower = np.percentile(bootstrap_means, lower_percentile)
        ci_upper = np.percentile(bootstrap_means, upper_percentile)
        
        return ci_lower, ci_upper, bootstrap_means


if __name__ == "__main__":
    # Sample set containing extreme outliers
    skewed_data = np.array([12, 14, 15, 13, 11, 19, 10, 115], dtype=np.float64)
    
    ci_low, ci_high, b_means = BootstrappingEngine.bootstrap_mean_confidence_interval(skewed_data, num_iterations=5000)
    
    assert ci_low < ci_high
    assert len(b_means) == 5000
    
    print(f"[TASK 06 PASSED] Bootstrapped Mean 95% CI bounds established: [{ci_low:.2f}, {ci_high:.2f}]")