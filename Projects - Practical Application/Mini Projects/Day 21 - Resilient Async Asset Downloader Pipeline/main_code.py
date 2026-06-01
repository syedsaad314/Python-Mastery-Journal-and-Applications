"""
System: Resilient Async Asset Downloader Pipeline
Description: A fault-tolerant asset downloader featuring async file chunk streaming,
             concurrency rate limits, and circuit breaker protection structures.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Downloader-Core) %(message)s')

class CircuitBreakerTripped(Exception): pass

class AsyncDownloadCircuitBreaker:
    def __init__(self, failure_limit: int = 2) -> None:
        self.limit: int = failure_limit
        self.failures: int = 0
        self.is_tripped: bool = False

    def register_success(self) -> None:
        self.failures = 0

    def register_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.limit:
            self.is_tripped = True


class ResilientAssetDownloader:
    def __init__(self, output_directory: str = "./downloaded_assets") -> None:
        self.output_dir: str = output_directory
        self.concurrency_gatekeeper: asyncio.Semaphore = asyncio.Semaphore(2) # Limit concurrent downloads to 2
        self.circuit_breaker: AsyncDownloadCircuitBreaker = AsyncDownloadCircuitBreaker()
        self.disk_io_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=2)

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    async def _mock_network_stream_payload(self, asset_id: str) -> AsyncGenerator[bytes, None]: # type: ignore
        """Simulates an asynchronous network stream chunk generator, raising network faults on specific resource IDs."""
        await asyncio.sleep(0.1)
        if asset_id == "ASSET_FAIL_03":
            raise ConnectionResetError("Remote server rejected asset stream mapping.")
            
        yield b"RAW_BINARY_DATA_CHUNK_HEADER\n"
        await asyncio.sleep(0.1)
        yield b"RAW_BINARY_DATA_CHUNK_BODY_TAIL\n"

    def _synchronous_disk_write(self, filepath: str, data_bytes: bytes) -> None:
        """Executes synchronous file append operations on a background thread pool worker."""
        with open(filepath, "ab") as f:
            f.write(data_bytes)

    async def download_asset(self, asset_id: str) -> bool:
        """Downloads assets concurrently while managing connection limits, circuit breakers, and async file chunking."""
        if self.circuit_breaker.is_tripped:
            logging.error(f"Download rejected for asset [{asset_id}]: Circuit breaker is TRIPPED.")
            raise CircuitBreakerTripped(f"Circuit tripped. Skipping download request for asset: {asset_id}")

        # Secure an execution slot from the concurrency semaphore gatekeeper
        async with self.concurrency_gatekeeper:
            loop = asyncio.get_running_loop()
            target_filepath = os.path.join(self.output_dir, f"{asset_id}.bin")
            
            # Clean up pre-existing file configurations before starting fresh transfers
            if os.path.exists(target_filepath):
                os.remove(target_filepath)

            try:
                logging.info(f"Starting asset stream download for target node: [{asset_id}]...")
                
                # Consume chunked data from the simulated network connection stream
                async for data_chunk in self._mock_network_stream_payload(asset_id):
                    # Offload blocking file system writes to the background thread pool
                    await loop.run_in_executor(
                        self.disk_io_executor, 
                        self._synchronous_disk_write, 
                        target_filepath, 
                        data_chunk
                    )

                self.circuit_breaker.register_success()
                logging.info(f"Asset [{asset_id}] downloaded and saved to disk successfully.")
                return True

            except Exception as network_fault:
                logging.error(f"Network error encountered downloading asset [{asset_id}]: {network_fault}")
                self.circuit_breaker.register_failure()
                if os.path.exists(target_filepath):
                    os.remove(target_filepath) # Clean up partial downloads on failure
                return False

    async def orchestrate_download_batch(self, batch_list: List[str]) -> Dict[str, Any]:
        """Orchestrates batches of downloads concurrently on the loop while managing faults and circuit breakers."""
        tasks = [self.download_asset(asset_id) for asset_id in batch_list]
        # Gather results, capturing exception states safely to keep the batch running
        execution_results = await asyncio.gather(*tasks, return_exceptions=True)

        success_count = 0
        blocked_count = 0
        failed_count = 0

        for res in execution_results:
            if isinstance(res, CircuitBreakerTripped):
                blocked_count += 1
            elif res is True:
                success_count += 1
            else:
                failed_count += 1

        return {
            "total_batch_size": len(batch_list),
            "successful_downloads": success_count,
            "failed_transfers": failed_count,
            "blocked_by_circuit_breaker": blocked_count,
            "circuit_breaker_final_status": "TRIPPED" if self.circuit_breaker.is_tripped else "HEALTHY"
        }

async def main() -> None:
    print("\n=== SYSTEM START: RESILIENT ASYNC ASSET DOWNLOADER ENGINE ===\n")
    downloader = ResilientAssetDownloader()

    assets_pipeline_queue = ["ASSET_NODE_01", "ASSET_NODE_02", "ASSET_FAIL_03", "ASSET_NODE_04"]
    metrics_summary = await downloader.orchestrate_download_batch(assets_pipeline_queue)

    print(f"\n=== DOWNLOAD PIPELINE METRICS SUMMARY ===\n")
    import json
    print(json.dumps(metrics_summary, indent=4))

    # Clean up generated asset files post-execution
    for asset in assets_pipeline_queue:
        path = f"./downloaded_assets/{asset}.bin"
        if os.path.exists(path):
            os.remove(path)
    if os.path.exists("./downloaded_assets"):
        os.rmdir("./downloaded_assets")

if __name__ == "__main__":
    asyncio.run(main())