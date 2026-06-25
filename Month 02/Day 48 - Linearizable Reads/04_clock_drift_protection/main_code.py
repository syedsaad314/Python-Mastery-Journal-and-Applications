# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Clock Drift Boundary Protection
Description: Adjusts the lease duration window down by a bounded clock drift factor 
             to prevent stale reads caused by CPU clock variances.
"""
class ClockDriftProtector:
    @staticmethod
    def calculate_safe_lease_window(nominal_lease: float, max_drift_percentage: float) -> float:
        # Reduce the lease window by the maximum expected clock drift factor to stay safe
        safety_reduction = nominal_lease * (max_drift_percentage / 100.0)
        safe_window = nominal_lease - safety_reduction
        print(f"[DRIFT-PROTECTION] Nominal lease: {nominal_lease}s | Adjusted safe window: {safe_window}s")
        return safe_window

if __name__ == "__main__":
    protector = ClockDriftProtector()
    safe_lease = protector.calculate_safe_lease_window(nominal_lease=2.0, max_drift_percentage=5.0)
    
    assert safe_lease == 1.90
    assert safe_lease < 2.0