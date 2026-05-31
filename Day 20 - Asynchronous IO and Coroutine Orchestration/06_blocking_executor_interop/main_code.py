"""
Core Topic: Interoperating Blocking Functions with Async Loops
Description: Offloads synchronous blocking code to background execution pools to prevent event loop lag.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

def synchronous_heavy_file_io(target_file: str) -> str:
    """A standard blocking function that would stall an event loop if called directly."""
    print(f"[BLOCKING-IO] Accessing legacy filesystem partition: {target_file}...")
    time.sleep(1.5)  # Blocking operation simulation
    return "DISK_SECTOR_EXTRACTED_CONTENT"

async def regular_async_heartbeat() -> None:
    """Background task to verify that the event loop remains responsive and does not freeze."""
    for tick in range(1, 5):
        print(f"[HEARTBEAT] Loop active and ticking normally... Tick #{tick}")
        await asyncio.sleep(0.4)

async def main() -> None:
    current_loop = asyncio.get_running_loop()
    
    # Provision a ThreadPoolExecutor to handle legacy blocking tasks
    with ThreadPoolExecutor(max_workers=1) as background_pool:
        print("[ORCHESTRATOR] Scheduling blocking I/O on an external thread pool...")
        
        # Schedule the blocking function inside the executor to prevent it from locking the event loop
        future_result = current_loop.run_in_executor(
            background_pool, 
            synchronous_heavy_file_io, 
            "legacy_ledger.db"
        )
        
        # Run an async heartbeat alongside the blocking task to prove the loop remains unblocked
        await asyncio.gather(regular_async_heartbeat(), future_result)
        
        retrieved_payload = await future_result
        print(f"[ORCHESTRATOR] Retracted data outcome: {retrieved_payload}")

if __name__ == "__main__":
    asyncio.run(main())