"""
CORE CONCEPT: Streaming Statistical Mechanics via Welford's Algorithm
Computing continuous, running sample and population variance in a single data pass.
Optimized for high-performance machine learning pipelines processing data streams
where loading whole sets into RAM is structurally impossible.
"""

class StreamingVarianceEngine:
    def __init__(self):
        self.count = 0
        self.mean = 0.0
        self.M2 = 0.0  # Running sum of squares of differences from the current mean

    def update(self, new_value: float) -> None:
        """Pushes a new data point into the tracking loop, updating metrics immediately."""
        self.count += 1
        delta = new_value - self.mean
        self.mean += delta / self.count
        delta2 = new_value - self.mean
        self.M2 += delta * delta2

    @property
    def sample_variance(self) -> float:
        """Calculates corrected sample variance (Bessel's correction)."""
        if self.count < 2:
            return 0.0
        return self.M2 / (self.count - 1)

    @property
    def population_variance(self) -> float:
        """Calculates standard population variance."""
        if self.count == 0:
            return 0.0
        return self.M2 / self.count


if __name__ == "__main__":
    stream = [10.0, 20.0, 30.0, 40.0, 50.0]
    engine = StreamingVarianceEngine()
    
    for data_point in stream:
        engine.update(data_point)
        
    print(f"Streaming Engine Mean: {engine.mean}")
    print(f"Streaming Engine Sample Variance: {engine.sample_variance}")