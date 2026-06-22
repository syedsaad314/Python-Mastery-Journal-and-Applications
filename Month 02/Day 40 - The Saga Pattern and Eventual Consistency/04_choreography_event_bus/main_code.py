"""
Core Topic: Choreographed Saga Event Bus Architecture
Description: Simulates an event-driven Saga where decentralized services react to events independently.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import List, Dict, Callable

class ChoreographyEventBus:
    """Manages event routing, letting services register handlers and publish events asynchronously."""
    
    def __init__(self) -> None:
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback_handler: Callable) -> None:
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback_handler)

    def publish_event(self, event_type: str, event_data: dict) -> None:
        """Dispatches an event payload directly to all registered microservice subscribers."""
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                handler(event_data)


if __name__ == "__main__":
    bus = ChoreographyEventBus()
    
    # Define microservice handlers reacting independently to network events
    def inventory_service_handler(data: dict):
        print(f"[INVENTORY-SERVICE] Order received for account {data['user']}. Deducting item SKU: {data['sku']}.")

    # Hook handlers up to the central bus
    bus.subscribe("ORDER_CREATED_EVENT", inventory_service_handler)
    
    print("[EVENT-BUS] Broadcasting 'ORDER_CREATED_EVENT' payload...")
    bus.publish_event("ORDER_CREATED_EVENT", {"user": "saad_irfan", "sku": "SKU-AI-LOG-40"})