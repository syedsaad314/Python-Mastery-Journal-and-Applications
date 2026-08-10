# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Kullback-Leibler (KL) Divergence
Description: Measures how one probability distribution diverges from a second, 
             acting as the foundation for Variational Autoencoders and t-SNE.
"""
import numpy as np  # type: ignore


class KLDivergenceEngine:
    @staticmethod
    def compute_kld(p: np.ndarray, q: np.ndarray) -> float:
        # P is the true distribution, Q is the approximation
        # Safety guards: KLD is only defined where p and q > 0
        epsilon = 1e-12
        p_safe = np.clip(p, epsilon, 1.0)
        q_safe = np.clip(q, epsilon, 1.0)
        
        # Normalize to strictly ensure sum(p) == 1 and sum(q) == 1
        p_safe /= np.sum(p_safe)
        q_safe /= np.sum(q_safe)
        
        # KL Divergence Formula: sum( P(x) * log(P(x) / Q(x)) )
        kld = np.sum(p_safe * np.log(p_safe / q_safe))
        return float(kld)


if __name__ == "__main__":
    # Identical distributions should yield KLD = 0.0
    dist_true = np.array([0.2, 0.5, 0.3])
    dist_approx_good = np.array([0.21, 0.48, 0.31])
    dist_approx_bad = np.array([0.8, 0.1, 0.1])
    
    kld_perfect = KLDivergenceEngine.compute_kld(dist_true, dist_true)
    kld_good = KLDivergenceEngine.compute_kld(dist_true, dist_approx_good)
    kld_bad = KLDivergenceEngine.compute_kld(dist_true, dist_approx_bad)
    
    assert abs(kld_perfect - 0.0) < 1e-9
    assert kld_good < kld_bad
    
    print(f"[TASK 03 PASSED] KL Divergence quantified. Perfect: {kld_perfect:.4f} | Near: {kld_good:.4f} | Far: {kld_bad:.4f}")