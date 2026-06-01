"""
Core Topic: Non-Blocking File Chunk Streaming via Executors
Description: Streams heavy disk files in chunks using background threads to prevent loop stalls.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

class AsyncFileChunkStreamer:
    def __init__(self, target_filepath: str, chunk_capacity: int = 1024) -> None:
        self.filepath: str = target_filepath
        self.chunk_size: int = chunk_capacity
        self.executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)

    def _sync_read_chunk(self, file_descriptor, offset: int) -> bytes:
        """Executes a synchronous, blocking file read operation on a background thread."""
        file_descriptor.seek(offset)
        return file_descriptor.read(self.chunk_size)

    async def stream_file(self) -> AsyncGenerator[bytes, None]: # type: ignore
        """Streams file contents in chunks asynchronously without blocking the main event loop."""
        loop = asyncio.get_running_loop()
        file_size = os.path.getsize(self.filepath)
        current_offset = 0

        with open(self.filepath, 'rb') as f:
            while current_offset < file_size:
                # Offload the blocking disk I/O operation to the thread pool executor
                chunk_payload = await loop.run_in_executor(
                    self.executor, 
                    self._sync_read_chunk, 
                    f, 
                    current_offset
                )
                if not chunk_payload:
                    break
                current_offset += len(chunk_payload)
                yield chunk_payload

async def main() -> None:
    temp_file = "async_stream_test.bin"
    with open(temp_file, "wb") as f:
        f.write(b"SAMPLE_BINARY_STREAM_DATA_METRIC_PACKET_ARRAY" * 100)

    streamer = AsyncFileChunkStreamer(temp_file, chunk_capacity=64)
    chunk_counter = 0
    
    async for chunk in streamer.stream_file():
        if chunk:
            chunk_counter += 1
            
    print(f"[STREAMER] Completed processing. Extracted total of {chunk_counter} non-blocking file chunks.")
    if os.path.exists(temp_file):
        os.remove(temp_file)

if __name__ == "__main__":
    asyncio.run(main())