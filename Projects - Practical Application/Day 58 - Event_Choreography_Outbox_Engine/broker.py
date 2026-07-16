# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Asynchronous Pub/Sub Distributed Message Router Engine
"""
import asyncio
from typing import Any, Dict, List, Callable, Coroutine
from models import ChoreographyEvent

class ChoreographyEventBroker:
    def __init__(self) -> None:
        self._registry: Dict[str, List[Callable[[ChoreographyEvent], Coroutine[Any, Any, None]]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[ChoreographyEvent], Coroutine[Any, Any, None]]) -> None:
        if event_type not in self._registry:
            self._registry[event_type] = []
        self._registry[event_type].append(handler)

    async def broadcast(self, event: ChoreographyEvent) -> None:
        if event.event_type not in self._registry:
            return
        
        print(f"   >>> [BROKER ROUTING] Directing event '{event.event_type}' to registered endpoints...")
        execution_tasks = [handler(event) for handler in self._registry[event.event_type]]
        await asyncio.gather(*execution_tasks)