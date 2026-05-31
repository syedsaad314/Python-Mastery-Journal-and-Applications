"""
Core Topic: Coroutine Basics and Event Loop Integration
Description: Demonstrates explicit cooperative yield processing using async and await.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import time

async def simulate_fetch_telemetry(sensor_id: str) -> dict:
    """Asynchronous coroutine routine yielding control implicitly during network simulation pauses."""
    print(f"[COROUTINE-{sensor_id}] Initiating database connection stream...")
    # asyncio.sleep is non-blocking; it yields control back to the central event loop scheduler
    await asyncio.sleep(0.5)
    print(f"[COROUTINE-{sensor_id}] Extraction complete. Packaging telemetry payload.")
    return {"sensor_id": sensor_id, "reading": 42.08, "status": "ONLINE"}

async def main() -> None:
    print("[EVENT LOOP] Spawning concurrent execution tasks...")
    # Wrap coroutines into structural Task wrappers to schedule them concurrently on the loop
    task_a = asyncio.create_task(simulate_fetch_telemetry("ALPHA-01"))
    task_b = asyncio.create_task(simulate_fetch_telemetry("BETA-02"))

    # Await tasks to resolve while they execute concurrently
    payload_a = await task_a
    payload_b = await task_b
    
    print(f"[EVENT LOOP] Compiled telemetry collection metrics: {payload_a}, {payload_b}")

if __name__ == "__main__":
    start_time = time.perf_counter()
    # Initialize the primary OS-level event loop engine context
    asyncio.run(main())
    duration = time.perf_counter() - start_time
    print(f"[MAIN THREAD] Execution runtime complete. Total time elapsed: {duration:.4f}s")