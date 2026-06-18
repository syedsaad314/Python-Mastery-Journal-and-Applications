"""
System: Enterprise Concurrent Task Queue & Job Scheduler Engine
Description: The application entry point. Initializes thread-safe priority structures, 
             spawns background workers, schedules real-world tasks, and launches the live UI dashboard.
Author: Syed Saad Bin Irfan
"""

import time
import random
from job_model import EnterpriseJob, Priority
from queue_manager import PriorityJobQueueManager
from worker_pool import ConcurrentWorkerPool
from dashboard_ui import TerminalDashboardUI

def generate_successful_task(task_name: str):
    """Simulates a heavy background computation task that completes successfully."""
    def action():
        time.sleep(random.uniform(0.5, 1.2)) # Emulate intensive operational run time
    action.__name__ = task_name
    return action

def generate_failing_task(task_name: str):
    """Simulates a task that encounters errors, forcing retry handling and DLQ routing."""
    def action():
        time.sleep(0.4)
        raise RuntimeError("Database Connection Timeout Error Exception.")
    action.__name__ = task_name
    return action

def main():
    # Step 1: Initialize Core Multi-Threaded Structural Engines
    manager = PriorityJobQueueManager()
    pool = ConcurrentWorkerPool(manager, worker_count=4)
    pool.start_pool()

    # Step 2: Ingest an initial batch of real-world corporate tasks
    manager.submit_job(EnterpriseJob("Generate Financial Statements Report", Priority.HIGH, generate_successful_task("Financials")))
    manager.submit_job(EnterpriseJob("Bulk Dispatch Corporate Notification Emails", Priority.LOW, generate_successful_task("BulkEmails")))
    manager.submit_job(EnterpriseJob("Process Ledger Transaction Write", Priority.MEDIUM, generate_successful_task("LedgerWrite")))
    manager.submit_job(EnterpriseJob("Synchronize Regional Cloud Analytics Store", Priority.HIGH, generate_failing_task("CloudSync")))
    manager.submit_job(EnterpriseJob("Compress Historic System Assets Archive", Priority.LOW, generate_successful_task("AssetCompression")))

    try:
        # Step 3: Run the execution tracking loop, streaming updates to the dashboard
        for cycle in range(12):
            TerminalDashboardUI.refresh_view(manager, pool)
            time.sleep(1.0)
            
            # Simulate dynamic runtime job arrival mid-execution
            if cycle == 3:
                manager.submit_job(EnterpriseJob("CRITICAL: Hotfix Security Patch Deployment", Priority.HIGH, generate_successful_task("SecurityHotfix")))
            if cycle == 5:
                manager.submit_job(EnterpriseJob("Rebuild ElasticSearch Index Cache", Priority.MEDIUM, generate_successful_task("CacheRebuild")))

        # Final snapshot draw before safe termination
        TerminalDashboardUI.refresh_view(manager, pool)
        print("\n[SYSTEM] Run complete. Shutting down worker thread infrastructure handles smoothly.")
    except KeyboardInterrupt:
        print("\n[SYSTEM] Dashboard termination intercepted. Powering down background run loops.")
    finally:
        pool.stop_pool()

if __name__ == "__main__":
    main()