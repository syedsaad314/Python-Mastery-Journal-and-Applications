# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Batch Normalization (Internal Covariate Shift Mitigation)
Description: Standardizes mini-batch distributions to mu=0/var=1, then applies
             learnable gamma/beta parameters while tracking running stats for inference.
"""
import numpy as np  # type: ignore
from typing import Tuple


class BatchNormalizationEngine:
    @staticmethod
    def batchnorm_forward(Z: np.ndarray, gamma: np.ndarray, beta: np.ndarray, 
                          running_mean: np.ndarray, running_var: np.ndarray, 
                          mode: str = 'train', epsilon: float = 1e-8, momentum: float = 0.9) -> Tuple[np.ndarray, dict]:
        
        if mode == 'train':
            # 1. Compute batch mean and variance across the batch dimension (axis 1)
            mu = np.mean(Z, axis=1, keepdims=True)
            var = np.var(Z, axis=1, keepdims=True)
            
            # 2. Normalize
            Z_norm = (Z - mu) / np.sqrt(var + epsilon)
            
            # 3. Update exponentially weighted running statistics
            running_mean = momentum * running_mean + (1 - momentum) * mu
            running_var = momentum * running_var + (1 - momentum) * var
            
            # Cache for backward pass
            cache = {"Z_norm": Z_norm, "var": var, "mu": mu, "eps": epsilon, "gamma": gamma}
        
        elif mode == 'test':
            # At inference, strictly use the historical running statistics
            Z_norm = (Z - running_mean) / np.sqrt(running_var + epsilon)
            cache = {}
        else:
            raise ValueError("Mode must be 'train' or 'test'.")
            
        # 4. Scale and shift using learnable parameters
        Z_tilde = gamma * Z_norm + beta
        
        return Z_tilde, cache, running_mean, running_var


if __name__ == "__main__":
    np.random.seed(42)
    # 3 Features, 100 Batch Size
    Z_raw = np.random.randn(3, 100) * 10 + 50  # Mean ~50, Var ~100
    
    gamma_init = np.ones((3, 1), dtype=np.float64)
    beta_init = np.zeros((3, 1), dtype=np.float64)
    r_mean = np.zeros((3, 1), dtype=np.float64)
    r_var = np.ones((3, 1), dtype=np.float64)
    
    Z_scaled, _, rm, rv = BatchNormalizationEngine.batchnorm_forward(
        Z_raw, gamma_init, beta_init, r_mean, r_var, mode='train'
    )
    
    # Validation: In train mode, the output feature batch mean should be exactly 0 (adjusted by beta 0)
    batch_mean_scaled = np.mean(Z_scaled, axis=1)
    batch_var_scaled = np.var(Z_scaled, axis=1)
    
    assert np.allclose(batch_mean_scaled, 0.0, atol=1e-7)
    assert np.allclose(batch_var_scaled, 1.0, atol=1e-7)
    
    print(f"[TASK 06 PASSED] Batch Normalization evaluated. Running Mean successfully updated: {rm.flatten()}")