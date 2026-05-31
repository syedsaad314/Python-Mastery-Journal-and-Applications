"""
Core Topic: High-Volume Concurrent Task Gathering
Description: Manages large batches of concurrent coroutines safely using asyncio.gather.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
from typing import List, Any

async def fetch_api_endpoint(endpoint_id: int) -> str:
    """Simulates an external HTTP request, raising intentional errors on specific routes."""
    await asyncio.sleep(0.2)
    if endpoint_id == 3:
        raise ValueError(f"CRITICAL HTTP 500: Corrupted data frame on endpoint {endpoint_id}")
    return f"DATA_PAYLOAD_NODE_{endpoint_id}"

async def main() -> None:
    # Build an array containing multiple separate coroutine workloads
    task_list = [fetch_api_endpoint(i) for i in range(1, 6)]
    
    print("[ORCHESTRATOR] Processing concurrent requests with return_exceptions=True...")
    # Setting return_exceptions=True traps errors, keeping sibling tasks running smoothly
    resolved_results: List[Any] = await asyncio.gather(*task_list, return_exceptions=True)
    
    print("\n--- Processing Results Matrix ---")
    for idx, item in enumerate(resolved_results, start=1):
        if isinstance(item, Exception):
            print(f"Index {idx} -> Handled Exception Trapped: {item}")
        else:
            print(f"Index {idx} -> Output Payload: {item}")

if __name__ == "__main__":
    asyncio.run(main())