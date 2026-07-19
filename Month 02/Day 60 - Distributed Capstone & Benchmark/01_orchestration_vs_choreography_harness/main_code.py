# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Orchestration vs Choreography Core Performance Harness
Description: Benchmarks structural latency variations between centralized execution 
             conductors and autonomous decentralized event routing.
"""
import asyncio
import time

async def simulated_network_hop(latency: float) -> None:
    await asyncio.sleep(latency)

async def run_orchestration_flow() -> float:
    start = time.perf_counter()
    # Conductor calls Service A, waits, then calls Service B
    await simulated_network_hop(0.01)
    await simulated_network_hop(0.01)
    return time.perf_counter() - start

async def run_choreography_flow() -> float:
    start = time.perf_counter()
    # Event loop broadcasts concurrently to independent listening threads
    await asyncio.gather(simulated_network_hop(0.01), simulated_network_hop(0.01))
    return time.perf_counter() - start

if __name__ == "__main__":
    t_orch = asyncio.run(run_orchestration_flow())
    t_chor = asyncio.run(run_choreography_flow())
    assert t_chor <= t_orch * 1.5
    print(f"[BENCHMARK] Orchestration: {t_orch:.4f}s | Choreography Parallel Run: {t_chor:.4f}s")