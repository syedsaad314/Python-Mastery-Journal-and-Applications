"""
Core Topic: Defensive Async Timeouts and Task Cancellations
Description: Protects application runtimes from hanging indefinitely using strict timeouts.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio

async def long_running_database_stream() -> str:
    """Simulates a slow stream query that can be safely cancelled mid-execution."""
    try:
        print("[STREAM] Initializing connection cursor blocks...")
        await asyncio.sleep(5.0)  # Simulate an extensive network data stall
        return "SUCCESSFUL_LARGE_QUERY_EXPORT"
    except asyncio.CancelledError:
        print("[STREAM] Cancellation signal caught! Performing database rollback operations...")
        raise  # Always reraise CancelledError to let the task exit cleanly

async def main() -> None:
    print("[MAIN] Dispatching database worker task with a strict 1.5s timeout allocation...")
    task = asyncio.create_task(long_running_database_stream())
    
    try:
        # Enforce a hard timeout ceiling on the target task
        validated_result = await asyncio.wait_for(task, timeout=1.5)
        print(f"[MAIN] Query resolved safely: {validated_result}")
    except asyncio.TimeoutError:
        print("[MAIN] Alert: Request exceeded timeout ceiling! Terminating resource handlers.")
        # asyncio.wait_for automatically triggers cancellation on the targeted task when a timeout hits

if __name__ == "__main__":
    asyncio.run(main())