"""
System: Atomically Guarded Transactional Outbox Store
Description: Simulates reliable event publishing by saving updates and outbound events together
             to a single database, using a background polling agent to publish events safely.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
import json
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (OutboxStore) %(message)s')

class ProductionOutboxDatabase:
    """Manages business tables and a message outbox log within a single transaction boundary."""
    
    def __init__(self) -> None:
        self.users_data_table: Dict[str, str] = {}
        self.outbox_event_table: List[Dict[str, Any]] = []

    def save_user_profile_atomic_transaction(self, user_id: str, profile_state: str, event_topic: str) -> None:
        """Guarantees message delivery by writing data changes and events to the database together."""
        # 1. Update the local business data table
        self.users_data_table[user_id] = profile_state
        
        # 2. Stage the outbound network event in the outbox log within the same transaction scope
        event_entry = {
            "msg_id": len(self.outbox_event_table) + 1,
            "topic": event_topic,
            "payload": json.dumps({"user_id": user_id, "status": profile_state}),
            "processed": False
        }
        self.outbox_event_table.append(event_entry)
        logging.info(f"[DB-TRANSACTION] Successfully committed local data and staged outbox event for user '{user_id}'.")


class BackgroundMessageRelayAgent:
    """Simulates a background service that reads the outbox log and publishes pending events to a broker."""
    
    def __init__(self, target_db: ProductionOutboxDatabase) -> None:
        self.db = target_db

    def scan_and_publish_pending_outbox_events(self) -> int:
        """Polls the outbox table, dispatches pending events, and flags them as processed."""
        dispatched_count = 0
        
        for record in self.db.outbox_event_table:
            if not record["processed"]:
                # Simulate a network event broadcast to an external message broker (e.g., Kafka or RabbitMQ)
                logging.info(f"[BROKER-RELAY] Transmitting message {record['msg_id']} over topic '{record['topic']}'...")
                
                # Flag the event as processed only after a successful network dispatch acknowledgment
                record["processed"] = True
                dispatched_count += 1
                
        return dispatched_count


if __name__ == "__main__":
    print("\n=== STARTING ATOMIC TRANSACTIONAL OUTBOX ENGINE ===\n")
    
    isolated_db = ProductionOutboxDatabase()
    relay_agent = BackgroundMessageRelayAgent(isolated_db)

    # 1. Simulate saving user profiles, which automatically writes events to the outbox log
    isolated_db.save_user_profile_atomic_transaction("user-saad-01", "UPGRADED_PREMIUM", "billing.events")
    isolated_db.save_user_profile_atomic_transaction("user-fabha-02", "REGISTERED_ACCOUNT", "auth.events")

    print("\n--- Running Background Message Relay Polling Cycle ---\n")
    
    # 2. Trigger the background relay agent to process and publish the staged outbox events
    total_published = relay_agent.scan_and_publish_pending_outbox_events()
    print(f"\n[RELAY-AGENT-COMPLETE] Total pending outbox events published to network broker: {total_published}")
    
    print("\n=== SYSTEM SHUTDOWN: TRANSACTIONAL OUTBOX ENGINE CLOSED ===")