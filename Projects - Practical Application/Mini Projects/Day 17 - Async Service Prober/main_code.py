"""
Mini-Project: Network Service Telemetry Prober
Description: Non-blocking asynchronous service health checker using cooperative multitasking.
Lead Engineer: Syed Saad Bin Irfan
"""

import asyncio
import json
import time
from typing import Dict, List, Any

class NetworkProber:
    def __init__(self, nodes: Dict[str, str]) -> None:
        self.nodes: Dict[str, str] = nodes

    async def _ping_endpoint(self, name: str, mock_delay: float) -> Dict[str, Any]:
        """Simulates an asynchronous network handshake with built-in retry fallback logic."""
        retries = 2
        for attempt in range(1, retries + 1):
            try:
                if mock_delay > 1.0 and attempt < retries:
                    raise asyncio.TimeoutError()
                # Yield control to the event loop to simulate network latency
                await asyncio.sleep(min(mock_delay, 0.5))
                return {"node": name, "status": "ONLINE", "rtt_sec": mock_delay, "attempts": attempt}
            except asyncio.TimeoutError:
                await asyncio.sleep(0.2) # Wait briefly before retrying
                
        return {"node": name, "status": "TIMEOUT_ALERT", "rtt_sec": mock_delay, "attempts": retries}

    async def execute_sweep(self, latencies: List[float]) -> List[Dict[str, Any]]:
        tasks = []
        for idx, (name, url) in enumerate(self.nodes.items()):
            delay = latencies[idx] if idx < len(latencies) else 0.1
            tasks.append(self._ping_endpoint(name, delay))
        
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    cluster = {
        "Authentication API": "http://10.0.0.5/health",
        "Relational Database Link": "http://10.0.0.12/health",
        "Caching Layer Cluster": "http://10.0.0.20/health"
    }
    
    prober = NetworkProber(cluster)
    simulated_delays = [0.1, 1.4, 0.2]  # Second element triggers a timeout retry flow
    
    print("[PORTFOLIO SHOWCASE] Initiating asynchronous network health sweep...")
    results = asyncio.run(prober.execute_sweep(simulated_delays))
    print(json.dumps(results, indent=2))