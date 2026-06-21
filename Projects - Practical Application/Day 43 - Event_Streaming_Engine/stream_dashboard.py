"""
Component: Stream Telemetry Dashboard
Description: Renders real-time scannable metrics tracking topic logs, partition offsets, and consumers.
Lead Engineer: Syed Saad Bin Irfan
"""

from ast import List
import os
from tabulate import tabulate # type: ignore
from colorama import init, Fore, Style # type: ignore
from message_broker import CentralMessageBroker
from consumer_group import DistributedStreamConsumer

init(autoreset=True)

class StreamTelemetryDashboardUI:
    
    @staticmethod
def display_metrics_frame(broker: CentralMessageBroker, consumers: List[DistributedStreamConsumer]) -> None: # type: ignore
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Fore.MAGENTA + Style.BRIGHT + "⭐ ======================================================= ⭐")
    print(Fore.MAGENTA + Style.BRIGHT + "    ENTERPRISE DISTRIBUTED EVENT STREAMING MONITOR PANEL")
    print(Fore.MAGENTA + Style.BRIGHT + "⭐ ======================================================= ⭐\n")

    # Table 1: Partition Log Depth and Committed Checkpoint Metrics
    partition_rows = []
    for p_id, partition_obj in broker.partitions.items():
        log_depth = len(partition_obj.log)
        committed_offset = broker.get_committed_offset("finance-analytics-group", p_id)
        lag = max(0, log_depth - committed_offset)
        
        partition_rows.append([
            f"Partition-{p_id}",
            f"{log_depth} Events Enqueued",
            f"Offset {committed_offset} Committed",
            Fore.RED + str(lag) + " Messages Lagging" if lag > 0 else Fore.GREEN + "Fully Synced"
        ])
    print(tabulate(partition_rows, headers=["Partition Coordinate", "Log Data Depth", "Group Commits", "Processing Lag Status"], tablefmt="presto"))
    print("\n" + Fore.YELLOW + "👥 --- Active Consumer Group Instance Balancing Threads ---")

    # Table 2: Worker Instance Partition Allocations and Processing Volume
    consumer_rows = []
    for worker in consumers:
        partitions_string = ", ".join([f"P-{p}" for p in worker.assigned_partitions]) if worker.assigned_partitions else "None (Idle)"
        consumer_rows.append([
            worker.worker_id,
            partitions_string,
            f"{worker.processed_event_count} Events Handled Successfully"
        ])
    print(tabulate(consumer_rows, headers=["Consumer Node ID", "Assigned Partition Locks", "Total Operational Throughput Volume"], tablefmt="simple"))
    print("\n" + Fore.WHITE + Style.DIM + "Streaming message logs... Press Ctrl+C to disconnect from broker engines.")