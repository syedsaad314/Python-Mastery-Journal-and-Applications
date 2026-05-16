"""
CORE CONCEPT: Spatial Distance Metric Engine
Building multidimensional distance calculators handling Euclidean and Manhattan
spaces from raw principles. This serves as the geometric decision engine for clustering
topologies and K-Nearest Neighbors (KNN) algorithms.
"""

import math

class SpatialDistanceEngine:
    @staticmethod
    def _validate_dimensions(point_a: list[float], point_b: list[float]) -> None:
        """Enforces structural alignment across multi-dimensional coordinate pairs."""
        if len(point_a) != len(point_b) or len(point_a) == 0:
            raise ValueError("Coordinates must be non-empty and possess identical dimensions.")

    @classmethod
    def euclidean_distance(cls, point_a: list[float], point_b: list[float]) -> float:
        """Computes straight-line L2 norm geometric distance."""
        cls._validate_dimensions(point_a, point_b)
        squared_sum = sum((a - b) ** 2 for a, b in zip(point_a, point_b))
        return math.sqrt(squared_sum)

    @classmethod
    def manhattan_distance(cls, point_a: list[float], point_b: list[float]) -> float:
        """Computes grid-based L1 norm taxicab distance."""
        cls._validate_dimensions(point_a, point_b)
        return sum(abs(a - b) for a, b in zip(point_a, point_b))


if __name__ == "__main__":
    coord_x = [1.0, 2.0, 3.0]
    coord_y = [4.0, 6.0, 8.0]
    
    print(f"L2 Euclidean Distance: {SpatialDistanceEngine.euclidean_distance(coord_x, coord_y)}")
    print(f"L1 Manhattan Distance: {SpatialDistanceEngine.manhattan_distance(coord_x, coord_y)}")