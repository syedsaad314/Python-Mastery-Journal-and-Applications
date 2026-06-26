# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: System Time Lease Management Allocators
"""
import time
from models import LeasePacket

class SystemLeaseManager:
    def __init__(self, baseline_duration: float, max_drift_factor: float) -> None:
        self.lease = LeasePacket(baseline_duration)
        self.drift_buffer = baseline_duration * (max_drift_factor / 100.0)

    def trigger_grant_renewal(self) -> None:
        self.lease.renew()

    def confirm_safe_read_authority(self) -> bool:
        # Check if the lease is valid while accounting for clock drift
        return self.lease.is_valid_with_drift(time.time(), self.drift_buffer)