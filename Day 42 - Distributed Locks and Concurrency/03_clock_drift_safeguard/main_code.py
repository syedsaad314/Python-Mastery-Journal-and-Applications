"""
Core Topic: Clock Drift Drift Mitigation Math
Description: Adjusts lock durations to account for clock drift errors across distributed servers.
Lead Engineer: Syed Saad Bin Irfan
"""

class ClockDriftSafeguard:
    """Calculates true lock validity duration by subtracting maximum drift factors."""
    
    @staticmethod
    def calculate_effective_validity(ttl_ms: float, max_drift_error_ms: float) -> float:
        """
        Applies mathematical corrections to ensure locks don't expire prematurely due to clock drift.
        Formula: Effective_TTL = Total_TTL - Drift_Error - Communication_Divergence
        """
        communication_divergence = 2.0 # Constant estimation for local system processing times
        effective_ttl = ttl_ms - max_drift_error_ms - communication_divergence
        return max(0.0, effective_ttl)


if __name__ == "__main__":
    safeguard = ClockDriftSafeguard()
    raw_ttl = 100.0  # ms
    drift = 5.0      # ms
    
    valid_window = safeguard.calculate_effective_validity(raw_ttl, drift)
    print(f"[CLOCK-GUARD] Raw Lock TTL: {raw_ttl}ms | Adjusted Safe Lifetime Window: {valid_window}ms")