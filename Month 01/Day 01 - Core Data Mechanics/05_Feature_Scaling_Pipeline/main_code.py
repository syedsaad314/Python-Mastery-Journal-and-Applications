"""
CORE CONCEPT: Object-Oriented Feature Normalization Engine
Constructing data preprocessing scalers using professional state-preservation structural
design. Implements modular Min-Max and Z-Score standardization while preserving parameters 
to eliminate pipeline leakage during inference transitions.
"""

import math

class AdvancedFeatureScaler:
    def __init__(self):
        self.min_val = None
        self.max_val = None
        self.mean = None
        self.stdev = None

    def fit(self, data: list[float]) -> None:
        """Analyzes historical state constraints and transforms them into stable properties."""
        if not data:
            raise ValueError("Input dataset cannot be evaluated empty.")
            
        self.min_val = min(data)
        self.max_val = max(data)
        
        self.mean = sum(data) / len(data)
        variance = sum((x - self.mean) ** 2 for x in data) / len(data)
        self.stdev = math.sqrt(variance) if variance > 0 else 1e-9

    def transform_min_max(self, data: list[float]) -> list[float]:
        """Normalizes features linearly bounded tightly inside normalized bounds [0, 1]."""
        if self.min_val is None or self.max_val is None:
            raise RuntimeError("Scaler state must be calculated using fit() before transformation execution.")
        range_val = (self.max_val - self.min_val) if (self.max_val - self.min_val) > 0 else 1e-9
        return [(x - self.min_val) / range_val for x in data]

    def transform_z_score(self, data: list[float]) -> list[float]:
        """Standardizes values to achieve a centered zero mean and unit variance layout."""
        if self.mean is None or self.stdev is None:
            raise RuntimeError("Scaler state must be calculated using fit() before transformation execution.")
        return [(x - self.mean) / self.stdev for x in data]


if __name__ == "__main__":
    raw_features = [12.0, 25.0, 34.0, 48.0, 90.0]
    scaler = AdvancedFeatureScaler()
    
    scaler.fit(raw_features)
    print(f"MinMax Pipeline Yield: {scaler.transform_min_max(raw_features)}")
    print(f"Z-Score Pipeline Yield: {scaler.transform_z_score(raw_features)}")