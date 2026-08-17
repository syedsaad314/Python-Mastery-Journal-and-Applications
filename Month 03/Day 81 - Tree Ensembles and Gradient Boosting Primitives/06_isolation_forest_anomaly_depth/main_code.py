# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Isolation Forest Path Length (Anomaly Detection)
Description: Calculates recursive anomaly isolation limits using harmonic numbers 
             to normalize split depth scores against a standard average tree depth.
"""
import numpy as np  # type: ignore


class IsolationForestEngine:
    @staticmethod
    def harmonic_number(n: int) -> float:
        # Euler-Mascheroni constant approximation for harmonic number series H(n-1)
        # H(i) ≈ ln(i) + 0.5772156649
        return np.log(n) + 0.5772156649

    @staticmethod
    def average_path_length_c(n_samples: int) -> float:
        # Calculates c(n): The average path length of unsuccessful search in a BST
        if n_samples <= 1:
            return 0.0
        if n_samples == 2:
            return 1.0
            
        c_n = 2.0 * IsolationForestEngine.harmonic_number(n_samples - 1) - (2.0 * (n_samples - 1.0) / n_samples)
        return float(c_n)

    @staticmethod
    def compute_anomaly_score(path_length: float, n_samples: int) -> float:
        # Score s(x, n) = 2^(-E(h(x)) / c(n))
        c_n = IsolationForestEngine.average_path_length_c(n_samples)
        
        # If score approaches 1.0, it is highly anomalous (isolated quickly)
        # If score approaches 0.5, it is a normal clustered point
        score = np.power(2.0, -(path_length / c_n))
        return float(score)


if __name__ == "__main__":
    total_samples = 1000
    
    # Anomaly: Isolated very quickly (Path length = 2 splits)
    anomaly_depth = 2.0
    
    # Inlier: Buried deep in a dense cluster (Path length = 15 splits)
    inlier_depth = 15.0
    
    score_anomaly = IsolationForestEngine.compute_anomaly_score(anomaly_depth, total_samples)
    score_inlier = IsolationForestEngine.compute_anomaly_score(inlier_depth, total_samples)
    
    # Anomalies yield scores closer to 1.0
    assert score_anomaly > 0.8
    # Normal points yield scores closer to 0.5
    assert score_inlier < 0.6
    
    print(f"[TASK 06 PASSED] Anomaly bounds checked. Anomaly Score: {score_anomaly:.3f} | Normal Score: {score_inlier:.3f}")