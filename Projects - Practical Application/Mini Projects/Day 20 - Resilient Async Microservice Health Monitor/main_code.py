"""
System: Resilient Async Microservice Health Monitor
Description: A high-performance, real-time microservice tracker that monitors server endpoints 
             concurrently, tracks response metrics, and catches timeouts defensively.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import json
import logging
import random
import time
from typing import Dict, List, Any, Optional

# Setup clean, structured production logging formats
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Loop-Thread) %(message)s')

class MicroserviceTargetNode:
    def __init__(self, service_name: str, health_endpoint_url: str, required_timeout: float = 1.0) -> None:
        self.name: str = service_name
        self.url: str = health_endpoint_url
        self.timeout_ceiling: float = required_timeout
        self.consecutive_failures: int = 0
        self.operational_status: str = "UNKNOWN"

class EnterpriseHealthMonitor:
    def __init__(self, targeted_cluster_nodes: List[MicroserviceTargetNode]) -> None:
        self.cluster_nodes: List[MicroserviceTargetNode] = targeted_cluster_nodes
        self.monitoring_metrics_ledger: Dict[str, List[Dict[str, Any]]] = {node.name: [] for node in targeted_cluster_nodes}
        self.metrics_mutex: asyncio.Lock = asyncio.Lock() # Guard structures within async contexts

    async def _ping_endpoint_simulation(self, node: MicroserviceTargetNode) -> Dict[str, Any]:
        """Simulates low-level HTTP network routing behavior with realistic network failures and latency spikes."""
        # Simulate realistic internet transport delays
        simulated_latency = random.uniform(0.1, 1.8)
        await asyncio.sleep(simulated_latency)

        # Simulate a network connection timeout spike
        if simulated_latency > node.timeout_ceiling:
            raise asyncio.TimeoutError(f"Network transport latency ({simulated_latency:.2f}s) breached timeout boundary.")

        # Simulate standard random server error responses
        if random.random() < 0.15:
            return {"http_status": 500, "latency_ms": int(simulated_latency * 1000), "payload": "INTERNAL_SERVER_ERROR"}

        return {"http_status": 200, "latency_ms": int(simulated_latency * 1000), "payload": "HEALTHY"}

    async def probe_single_node_health(self, node: MicroserviceTargetNode) -> None:
        """Probes an endpoint, tracks health metrics, and handles network timeouts defensively."""
        timestamp_of_probe = time.strftime('%Y-%m-%d %H:%M:%S')
        metrics_record: Dict[str, Any] = {"timestamp": timestamp_of_probe, "node_name": node.name}

        try:
            logging.info(f"[MONITOR] Probing service endpoint [{node.name}] at destination route ({node.url})...")
            
            # Enforce strict timeout ceilings on the simulated network request
            network_response = await asyncio.wait_for(
                self._ping_endpoint_simulation(node), 
                timeout=node.timeout_ceiling
            )

            if network_response["http_status"] == 200:
                node.operational_status = "HEALTHY"
                node.consecutive_failures = 0
                metrics_record.update({"status": "UP", "latency": network_response["latency_ms"], "error": None})
            else:
                node.operational_status = "DEGRADED"
                node.consecutive_failures += 1
                metrics_record.update({"status": "DEGRADED", "latency": network_response["latency_ms"], "error": "HTTP_500_ERROR"})

        except asyncio.TimeoutError:
            node.consecutive_failures += 1
            node.operational_status = "UNRESPONSIVE" if node.consecutive_failures >= 2 else "DEGRADED"
            logging.warning(f"[ALERT] Service Node [{node.name}] timed out during health check.")
            metrics_record.update({"status": "TIMEOUT", "latency": int(node.timeout_ceiling * 1000), "error": "TimeoutException"})

        except Exception as unhandled_error:
            node.operational_status = "CRITICAL_FAULT"
            metrics_record.update({"status": "CRITICAL", "latency": 0, "error": str(unhandled_error)})

        # Securely log metrics to the ledger using async context locks
        async with self.metrics_mutex:
            self.monitoring_metrics_ledger[node.name].append(metrics_record)

    async def execute_cluster_monitoring_pass(self) -> None:
        """Executes a single monitoring sweep across all registered microservice endpoints concurrently."""
        logging.info("--- Starting Concurrent Cluster Health Sweep ---")
        # Map tasks to run concurrently across the active event loop
        probing_tasks = [self.probe_single_node_health(node) for node in self.cluster_nodes]
        await asyncio.gather(*probing_tasks)
        logging.info("--- Cluster Health Sweep Completed ---")

    async def continuous_monitoring_daemon_loop(self, cycles: int = 3) -> None:
        """Runs the monitoring loop continuously for a specified number of intervals."""
        for interval in range(1, cycles + 1):
            logging.info(f"\n[DAEMON] Triggering evaluation sweep iteration #{interval}")
            await self.execute_cluster_monitoring_pass()
            # Yield control back to the loop during idle intervals
            await asyncio.sleep(2.0)

if __name__ == "__main__":
    print("\n=== STARTING ENTERPRISE ASYNC MICROSERVICE MONITOR ENGINE ===\n")
    
    # Configure microservice endpoint definitions
    monitored_endpoints = [
        MicroserviceTargetNode("User Auth Service", "https://api.uok.edu.pk/v1/auth/health", required_timeout=1.0),
        MicroserviceTargetNode("Payment Processing Engine", "https://api.uok.edu.pk/v1/payments/status", required_timeout=0.8),
        MicroserviceTargetNode("Realtime Analytics Dashboard", "https://api.uok.edu.pk/v1/analytics/ping", required_timeout=1.2)
    ]

    monitor_engine = EnterpriseHealthMonitor(targeted_cluster_nodes=monitored_endpoints)

    # Initialize the engine loop to run three complete collection cycles
    asyncio.run(monitor_engine.continuous_monitoring_daemon_loop(cycles=3))

    print("\n=== METRICS EXTRACTION MATRIX SUMMARY ===")
    print(json.dumps(monitor_engine.monitoring_metrics_ledger, indent=4))