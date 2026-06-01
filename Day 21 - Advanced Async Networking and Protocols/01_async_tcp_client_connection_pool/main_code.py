"""
Core Topic: Async TCP Connection Pooling Simulation
Description: Manages a reusable pool of async stream sockets to reduce network handshake overhead.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
from typing import List, Tuple

class AsyncStreamConnectionPool:
    def __init__(self, host: str, port: int, pool_capacity: int = 3) -> None:
        self.host: str = host
        self.port: int = port
        self.capacity: int = pool_capacity
        self.pool: asyncio.Queue = asyncio.Queue()
        self.allocated_count: int = 0

    async def initialize_pool(self) -> None:
        """Pre-allocates streaming socket connection boundaries inside the pool queue."""
        print(f"[POOL] Pre-populating {self.capacity} socket connections to {self.host}:{self.port}...")
        # Simulating connections for isolation proofing inside standard loop frameworks
        for i in range(self.capacity):
            mock_connection_node = (f"ReaderChannel-{i}", f"WriterChannel-{i}")
            await self.pool.put(mock_connection_node)
            self.allocated_count += 1

    async def acquire_connection(self) -> Tuple[str, str]:
        """Leases a network stream pair from the queue, yielding if empty."""
        connection_node = await self.pool.get()
        print(f"[POOL] Connection leased from pool. Available items left: {self.pool.qsize()}")
        return connection_node

    async def release_connection(self, connection_node: Tuple[str, str]) -> None:
        """Returns an open stream connection to the reusable pool."""
        await self.pool.put(connection_node)
        print(f"[POOL] Connection returned to pool. Total active stock: {self.pool.qsize()}")

async def main() -> None:
    pool_manager = AsyncStreamConnectionPool("127.0.0.1", 9000, pool_capacity=2)
    await pool_manager.initialize_pool()

    # Acquire leased slots concurrently
    conn_one = await pool_manager.acquire_connection()
    conn_two = await pool_manager.acquire_connection()

    # Release them back safely to avoid resource starvation holes
    await pool_manager.release_connection(conn_one)
    await pool_manager.release_connection(conn_two)

if __name__ == "__main__":
    asyncio.run(main())