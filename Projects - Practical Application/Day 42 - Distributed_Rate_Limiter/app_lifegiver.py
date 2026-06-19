"""
System: Enterprise Distributed Rate Limiter Entry Point
Description: Connects the system components. Initializes node configurations, schedules background 
             synchronization, runs real-world traffic profiles, and drives the interactive UI dashboard.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
from rate_bucket import TokenBucketLimiter
from cluster_sync import ClusterSynchronizationCoordinator
from traffic_generator import TrafficBurstSimulator
from monitor_dashboard import OperationalDashboardUI

def main() -> None:
    # Step 1: Initialize independent gateway nodes with custom capacities and refill metrics
    gateway_cluster = {
        "api-gateway-us-east": TokenBucketLimiter(capacity=40, refill_rate_per_sec=10.0),
        "api-gateway-eu-west": TokenBucketLimiter(capacity=40, refill_rate_per_sec=10.0),
        "api-gateway-ap-south": TokenBucketLimiter(capacity=40, refill_rate_per_sec=10.0)
    }

    # Step 2: Bind the system components to their synchronization and simulation coordinators
    sync_coordinator = ClusterSynchronizationCoordinator(gateway_cluster)
    traffic_engine = TrafficBurstSimulator(gateway_cluster)

    print("[SYSTEM] Booting cluster node mesh infrastructures safely...")
    time.sleep(1.0)

    try:
        # Step 3: Run structured traffic simulation cycles
        for cycle in range(15):
            # Simulate a normal traffic profile for the first 6 cycles, then trigger an intense traffic spike
            is_spike = (cycle >= 6 and cycle <= 11)
            traffic_state_label = "🚨 HIGH VOLTAGE TRAFFIC SURGE SPIKE ACTIVE" if is_spike else "🟢 STABLE STEADY-STATE TRAFFIC LOADS"

            # Route traffic updates through the simulator
            traffic_engine.simulate_traffic_packet(intense_spike_mode=is_spike)

            # Trigger the cluster synchronization loop to balance state across nodes
            sync_coordinator.broadcast_global_reconciliation_cycle()

            # Refresh the interactive telemetry dashboard view
            OperationalDashboardUI.render_system_frame(sync_coordinator, traffic_engine, traffic_state_label)
            time.sleep(0.8)

        print("\n" + Fore.GREEN + "[SUCCESS] Simulation run finalized cleanly. All gateway logs saved.") # type: ignore
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Intercepted termination signal. Shutting down gateway cluster meshes smoothly.")

if __name__ == "__main__":
    main()