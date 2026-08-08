# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Monte Carlo Integration
Description: Estimates the area under a curve (or Pi) using large-scale 
             stochastic uniform random sampling.
"""
import numpy as np  # type: ignore


class MonteCarloEngine:
    @staticmethod
    def estimate_pi(num_samples: int) -> float:
        # Generate N random coordinates in a [0,1) x [0,1) square
        # Using a unified random generator to ensure independent sampling
        rng = np.random.default_rng(42)
        x_coords = rng.random(num_samples)
        y_coords = rng.random(num_samples)
        
        # Compute distance squared from origin (0,0)
        distance_squared = np.square(x_coords) + np.square(y_coords)
        
        # Points inside the quarter-circle have distance_squared <= 1
        points_inside = np.sum(distance_squared <= 1.0)
        
        # Area of circle = Pi * r^2. Area of square = (2r)^2. Ratio = Pi / 4.
        # Therefore, Pi = 4 * (Points Inside / Total Points)
        estimated_pi = 4.0 * (points_inside / num_samples)
        return estimated_pi


if __name__ == "__main__":
    n_samples = 1_000_000
    pi_approximation = MonteCarloEngine.estimate_pi(n_samples)
    
    # Pi should be accurately approximated to roughly 2 decimal points with 1M samples
    assert abs(pi_approximation - np.pi) < 0.01
    
    print(f"[TASK 03 PASSED] Monte Carlo Integration estimated Pi: {pi_approximation:.5f} using {n_samples} samples.")