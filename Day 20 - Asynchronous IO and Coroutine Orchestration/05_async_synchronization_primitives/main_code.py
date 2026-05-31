"""
Core Topic: Async Synchronization Primitives and Semaphores
Description: Limits concurrent coroutine access to sensitive resources using async semaphores.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio

class ThrottledApiDispatcher:
    def __init__(self, concurrency_limit: int) -> None:
        # Async Semaphores manage internal counter balances inside a single thread context
        self.api_gatekeeper = asyncio.Semaphore(concurrency_limit)

    def __get_running_loop(self) -> asyncio.AbstractEventLoop:
        return asyncio.get_running_loop()

    async def execute_rate_limited_query(self, worker_id: int) -> None:
        print(f"[WORKER-{worker_id}] Awaiting an open API slot...")
        # Secure an execution slot; yield control if the semaphore counter is zero
        async with self.api_gatekeeper:
            print(f"[WORKER-{worker_id}] Slot acquired. Dispatching payload request...")
            await asyncio.sleep(0.5)  # Simulate remote execution delay
            print(f"[WORKER-{worker_id}] Transaction complete. Releasing slot.")

async def main() -> None:
    # Cap total concurrent connections to a maximum of 2 slots
    dispatcher = ThrottledApiDispatcher(concurrency_limit=2)
    
    # Launch 5 concurrent operations simultaneously
    batch_operations = [dispatcher.execute_rate_limited_query(i) for i in range(1, 6)]
    await asyncio.gather(*batch_operations)

if __name__ == "__main__":
    asyncio.run(main())