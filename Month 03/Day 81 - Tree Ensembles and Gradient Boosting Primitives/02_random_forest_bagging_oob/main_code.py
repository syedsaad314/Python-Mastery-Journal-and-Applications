# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Bootstrap Aggregating (Bagging) & Out-of-Bag (OOB) Tracking
Description: Constructs randomized training subsets with replacement, isolating 
             unseen samples to evaluate ensemble accuracy without a holdout validation set.
"""
import numpy as np  # type: ignore


class BaggingEngine:
    @staticmethod
    def generate_bootstrap_sample(n_samples: int) -> tuple[np.ndarray, np.ndarray]:
        rng = np.random.default_rng(42)
        
        # Draw samples WITH replacement
        in_bag_indices = rng.integers(0, n_samples, size=n_samples)
        
        # Identify Out-of-Bag (OOB) samples using set difference
        all_indices = np.arange(n_samples)
        oob_indices = np.setdiff1d(all_indices, in_bag_indices)
        
        return in_bag_indices, oob_indices


if __name__ == "__main__":
    n = 10000
    in_bag, oob = BaggingEngine.generate_bootstrap_sample(n)
    
    assert len(in_bag) == n
    
    # Mathematical proof: As N approaches infinity, the probability of a sample 
    # NOT being selected in N draws is (1 - 1/N)^N ≈ 1/e ≈ 0.3678 (36.8%)
    oob_ratio = len(oob) / n
    
    assert 0.35 < oob_ratio < 0.38
    
    # Assert mutual exclusivity of sets
    assert len(np.intersect1d(in_bag, oob)) == 0
    
    print(f"[TASK 02 PASSED] Bagging generator processed {n} samples. OOB Ratio converges to 1/e: {oob_ratio:.4f}")