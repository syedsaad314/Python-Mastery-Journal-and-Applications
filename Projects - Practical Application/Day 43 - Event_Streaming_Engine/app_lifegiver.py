"""
System: Enterprise Event Streaming Engine Entry Point
Description: Launches the event broker networks, configures consumer groups, 
             streams high-volume transaction entries, and drives the real-time telemetry dashboard.
Lead Engineer: Syed Saad Bin Irfan
"""

import time
import random
from message_broker import CentralMessageBroker
from producer import IdempotentEventProducer
from consumer_group import DistributedStreamConsumer
from stream_dashboard import StreamTelemetryDashboardUI

def main() -> None:
    # Step 1: Initialize the central message broker with 3 horizontally scaled partitions
    broker = CentralMessageBroker(topic_name="monetary_transactions", total_partitions=3)
    
    # Step 2: Initialize an idempotent producer instance
    producer = IdempotentEventProducer(producer_id="payment-api-service-01", broker_reference=broker)

    # Step 3: Configure a dedicated consumer group with 2 background consumer instances
    group_name = "finance-analytics-group"
    consumer_pool = [
        DistributedStreamConsumer(group_name, "analytics-node-A", broker),
        DistributedStreamConsumer(group_name, "analytics-node-B", broker)
    ]

    # Step 4: Run a partition rebalance cycle to assign topics across active group workers
    all_partitions = list(broker.partitions.keys())
    for idx, p_id in enumerate(all_partitions):
        target_consumer = consumer_pool[idx % len(consumer_pool)]
        target_consumer.assigned_partitions.append(p_id)

    # Boot consumer polling loops
    for consumer in consumer_pool:
        consumer.start_polling_loop()

    try:
        # Step 5: Simulate high-volume traffic pipelines by streaming transaction logs
        mock_routing_keys = ["user_102_tx", "user_405_tx", "user_789_tx", "user_112_tx", "user_554_tx"]
        
        for cycle in range(12):
            # Publish a batch of financial events distributed dynamically across partitions via key hashing
            for _ in range(random.randint(2, 5)):
                key = random.choice(mock_routing_keys)
                amount = random.randint(100, 1500)
                producer.broadcast_event(
                    routing_key=key,
                    event_type="ORDER_PROCESSED",
                    data={"transaction_value": amount, "currency": "PKR"}
                )

            # Refresh the interactive telemetry dashboard view
            StreamTelemetryDashboardUI.display_metrics_frame(broker, consumer_pool)
            time.sleep(1.0)

        # Final draw before closing operations
        StreamTelemetryDashboardUI.display_metrics_frame(broker, consumer_pool)
        print("\n[SUCCESS] Main injection stream completed. Winding down engine handles smoothly.")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Intercepted exit call. Powering down background brokers safely.")
    finally:
        for consumer in consumer_pool:
            consumer.stop()

if __name__ == "__main__":
    main()