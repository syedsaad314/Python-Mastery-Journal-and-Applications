# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Event Broker Router Simulation
Description: Models an asynchronous pub/sub messaging hub matching event topics 
             to dynamically isolated listener channels.
"""
import asyncio
from typing import Dict, List, Callable, Coroutine, Any

class AsyncEventBrokerRouter:
    def __init__(self) -> None:
        self._subscriptions: Dict[str, List[Callable[[Any], Coroutine[Any, Any, None]]]] = {}

    def subscribe(self, topic: str, handler: Callable[[Any], Coroutine[Any, Any, None]]) -> None:
        if topic not in self._subscriptions:
            self._subscriptions[topic] = []
        self._subscriptions[topic].append(handler)

    async def publish(self, topic: str, event_data: Any) -> None:
        if topic not in self._subscriptions:
            return
        
        # Fire all registered handler tasks concurrently
        tasks = [handler(event_data) for handler in self._subscriptions[topic]]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    broker = AsyncEventBrokerRouter()
    execution_flag = False

    async def mock_receiver(data: dict) -> None:
        global execution_flag
        execution_flag = data.get("executed", False)

    broker.subscribe("test.topic", mock_receiver)
    asyncio.run(broker.publish("test.topic", {"executed": True}))
    assert execution_flag is True