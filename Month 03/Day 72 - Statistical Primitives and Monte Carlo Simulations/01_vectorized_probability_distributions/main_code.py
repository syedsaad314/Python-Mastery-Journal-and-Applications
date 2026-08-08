# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vectorized Probability Density Functions (PDF)
Description: Computes the Gaussian (Normal) Distribution PDF across a high-dimensional 
             vector array using pure NumPy primitives without iterative loops.
"""
import numpy as np  # type: ignore


class ProbabilityDistributionEngine:
    @staticmethod
    def compute_gaussian_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
        if sigma <= 0:
            raise ValueError("Standard deviation (sigma) must be strictly positive.")
            
        # PDF Formula: (1 / (sigma * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sigma)^2)
        variance = sigma ** 2
        normalization_constant = 1.0 / np.sqrt(2 * np.pi * variance)
        exponent_term = np.exp(-0.5 * np.square((x - mu) / sigma))
        
        return normalization_constant * exponent_term


if __name__ == "__main__":
    # Create an array of values spanning 3 standard deviations
    data_points = np.array([-3.0, 0.0, 3.0], dtype=np.float64)
    
    # Compute PDF for Standard Normal Distribution (mu=0, sigma=1)
    pdf_values = ProbabilityDistributionEngine.compute_gaussian_pdf(data_points, mu=0.0, sigma=1.0)
    
    assert pdf_values.shape == (3,)
    # The peak of standard normal distribution at x=0 is ~0.3989
    assert abs(pdf_values[1] - 0.398942) < 1e-4
    # The tails should be identical (symmetric distribution)
    assert abs(pdf_values[0] - pdf_values[2]) < 1e-9
    
    print(f"[TASK 01 PASSED] Vectorized Gaussian PDF computed. Peak value at mu: {pdf_values[1]:.4f}")