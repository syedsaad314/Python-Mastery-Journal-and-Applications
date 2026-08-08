# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Welch's T-Test (Hypothesis Testing)
Description: Vectorizes the Welch's T-Test calculation to determine statistical 
             significance between two sample distributions with unequal variances.
"""
import numpy as np  # type: ignore


class StatisticalTestEngine:
    @staticmethod
    def compute_welchs_t_statistic(sample_a: np.ndarray, sample_b: np.ndarray) -> tuple[float, float]:
        n_a, n_b = len(sample_a), len(sample_b)
        mean_a, mean_b = np.mean(sample_a), np.mean(sample_b)
        
        # ddof=1 provides unbiased sample variance estimator (n-1)
        var_a = np.var(sample_a, ddof=1)
        var_b = np.var(sample_b, ddof=1)
        
        # Welch's T-Statistic Formula
        numerator = mean_a - mean_b
        denominator = np.sqrt((var_a / n_a) + (var_b / n_b))
        
        t_stat = numerator / denominator
        
        # Degrees of freedom approximation (Welch-Satterthwaite equation)
        df_num = ((var_a / n_a) + (var_b / n_b)) ** 2
        df_den = ((var_a / n_a)**2 / (n_a - 1)) + ((var_b / n_b)**2 / (n_b - 1))
        degrees_of_freedom = df_num / df_den
        
        return t_stat, degrees_of_freedom


if __name__ == "__main__":
    # Define two distinct normal distributions
    rng = np.random.default_rng(42)
    group_a = rng.normal(loc=50.0, scale=5.0, size=100)
    group_b = rng.normal(loc=55.0, scale=10.0, size=120)
    
    t_val, dof = StatisticalTestEngine.compute_welchs_t_statistic(group_a, group_b)
    
    assert dof > 0
    assert t_val < 0  # Group A's mean is lower, expecting a negative t-statistic
    
    print(f"[TASK 05 PASSED] Welch's t-statistic calculated. t-score: {t_val:.4f}, DoF: {dof:.2f}")