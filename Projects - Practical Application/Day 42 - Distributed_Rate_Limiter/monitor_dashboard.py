"""
Component: Telemetry Monitor Dashboard Dashboard
Description: Renders an interactive, clean terminal interface showing rate limiting metrics.
Lead Engineer: Syed Saad Bin Irfan
"""

import os
from tabulate import tabulate # type: ignore
from colorama import init, Fore, Style # type: ignore
from cluster_sync import ClusterSynchronizationCoordinator
from traffic_generator import TrafficBurstSimulator

init(autoreset=True)

class OperationalDashboardUI:
    """Renders real-time telemetry tables for the running rate limiter cluster."""
    
    @staticmethod
    def render_system_frame(coordinator: ClusterSynchronizationCoordinator, simulator: TrafficBurstSimulator, condition: str) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(Fore.GREEN + Style.BRIGHT + "✨ ======================================================= ✨")
        print(Fore.GREEN + Style.BRIGHT + "    ENTERPRISE DISTRIBUTED RATE LIMITER METRICS PANEL")
        print(Fore.GREEN + Style.BRIGHT + "✨ ======================================================= ✨\n")
        
        # Display the active traffic environment status
        status_color = Fore.RED if "HIGH" in condition else Fore.CYAN
        print(f"Current Traffic Profile: {status_color}{Style.BRIGHT}{condition}\n")

        # Table 1: Global Cluster Traffic Routing Statistics
        traffic_metrics = [
            ["Successful Safe Requests Allowed", Fore.GREEN + str(simulator.allowed_requests_counter)],
            ["Blocked Rate-Limited Drops", Fore.RED + str(simulator.dropped_requests_counter)]
        ]
        print(tabulate(traffic_metrics, headers=["Metric category", "Cluster Count Summary"], tablefmt="presto"))
        print("\n" + Fore.YELLOW + "📊 --- Active Node Token Pool Balances ---")

        # Table 2: Individual Gateway Node Resource Balances
        node_rows = []
        for name, instance in coordinator.nodes.items():
            with instance._lock:
                current_tokens = round(instance.tokens, 2)
            node_rows.append([name, f"{current_tokens} / {instance.capacity} Tokens"])
            
        print(tabulate(node_rows, headers=["Gateway ID", "Available Token Capacity Balance"], tablefmt="simple"))
        print("\n" + Fore.WHITE + Style.DIM + "Streaming telemetry logs... Press Ctrl+C to terminate the simulation cluster safely.")