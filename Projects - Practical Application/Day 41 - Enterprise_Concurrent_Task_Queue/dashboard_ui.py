"""
Component: Interactive CLI Dashboard Layout
Description: Formats and displays queue status and worker activity cleanly in the terminal.
Author: Syed Saad Bin Irfan
"""

import os
from tabulate import tabulate # type: ignore
from colorama import init, Fore, Style # type: ignore
from queue_manager import PriorityJobQueueManager
from worker_pool import ConcurrentWorkerPool

init(autoreset=True)

class TerminalDashboardUI:
    """Renders a structured, clean command-line interface tracking queue status and worker activity."""
    
    @staticmethod
    def refresh_view(manager: PriorityJobQueueManager, pool: ConcurrentWorkerPool) -> None:
        """Clears the terminal and draws a scannable snapshot of the running task engine."""
        os.system('cls' if os.name == 'nt' else 'clear')
        pending, dead = manager.get_snapshot_counts()
        
        print(Fore.CYAN + Style.BRIGHT + "========================================================")
        print(Fore.CYAN + Style.BRIGHT + "   ENTERPRISE CONCURRENT TASK QUEUE MANAGEMENT SYSTEM")
        print(Fore.CYAN + Style.BRIGHT + "========================================================\n")
        
        # Section 1: Core System Metrics
        metrics_table = [
            ["Active Workers Configured", pool.worker_count],
            ["Pending Tasks Staged (Heap)", pending],
            ["Dead-Letter Queue Count (DLQ)", Fore.RED + str(dead) if dead > 0 else "0"]
        ]
        print(tabulate(metrics_table, headers=["System Component", "Current Status Count"], tablefmt="presto"))
        print("\n" + Fore.YELLOW + "--- Active Thread Worker Execution Pool Pool ---")
        
        # Section 2: Worker Thread Utilization Matrix
        worker_data = [[w_id, status] for w_id, status in pool.active_worker_status.items()]
        print(tabulate(worker_data, headers=["Thread Identifier", "Current Active Task Assignment"], tablefmt="simple"))
        
        # Section 3: Dead Letter Queue Inspection
        dlq_records = manager.get_dlq_records()
        if dlq_records:
            print("\n" + Fore.RED + "--- Critical Audit: Dead-Letter Queue (DLQ) Records ---")
            dlq_table = [[j.job_id, j.name, j.execution_error] for j in dlq_records]
            print(tabulate(dlq_table, headers=["Job ID", "Task Failure Name", "Error Cause Traceback"], tablefmt="plain"))
        print("\n" + Fore.WHITE + Style.DIM + "Monitoring execution engines... Press Ctrl+C to disconnect container metrics.")