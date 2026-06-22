"""
Core Topic: High-Performance Async Producer-Consumer Queues
Description: Coordinates data routing across async tasks using a non-blocking queue.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import random

async def data_packet_producer(pipeline_queue: asyncio.Queue, producer_id: int) -> None:
    """Generates mock transactional log metrics and pushes them to the shared queue."""
    for item_idx in range(1, 4):
        await asyncio.sleep(random.uniform(0.1, 0.3))
        generated_token = f"TOKEN_ID_{producer_id}_{item_idx}"
        await pipeline_queue.put(generated_token)
        print(f"[PRODUCER-{producer_id}] Enqueued: {generated_token}")

async def data_packet_consumer(pipeline_queue: asyncio.Queue, consumer_id: int) -> None:
    """Processes items from the queue until the manager explicit cancels execution."""
    while True:
        # Fetch an item from the queue; yield control if the queue is empty
        packet = await pipeline_queue.get()
        try:
            print(f"[CONSUMER-{consumer_id}] Processing: {packet}")
            await asyncio.sleep(0.2)  # Simulate processing overhead
        finally:
            # Signal that the item has been completely processed
            pipeline_queue.task_done()

async def main() -> None:
    shared_async_queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    
    # Spawn multiple producer tasks
    producers = [asyncio.create_task(data_packet_producer(shared_async_queue, i)) for i in range(2)]
    # Spawn consumer tasks to process incoming data
    consumers = [asyncio.create_task(data_packet_consumer(shared_async_queue, i)) for i in range(2)]
    
    # Wait for all producers to finish generating data
    await asyncio.gather(*producers)
    
    # Block execution until all queue items are processed and marked task_done()
    await shared_async_queue.join()
    
    # Cleanly terminate the persistent consumer loops
    for worker_task in consumers:
        worker_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())