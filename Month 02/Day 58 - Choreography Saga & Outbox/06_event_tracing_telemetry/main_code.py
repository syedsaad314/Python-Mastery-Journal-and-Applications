# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Event Tracing Telemetry
Description: Generates unified audit trail traces to track the asynchronous path 
             of events across multiple independent systems.
"""
from typing import List, Dict, Any

class DistributedEventTracerTelemetry:
    def __init__(self) -> None:
        self.trace_logs: List[Dict[str, Any]] = []

    def record_trace(self, correlation_id: str, element_source: str, operation: str) -> None:
        self.trace_logs.append({
            "correlation_id": correlation_id,
            "source": element_source,
            "op": operation
        })

    def extract_full_pipeline_path(self, correlation_id: str) -> List[str]:
        return [f"{log['source']}->{log['op']}" for log in self.trace_logs if log["correlation_id"] == correlation_id]

if __name__ == "__main__":
    tracer = DistributedEventTracerTelemetry()
    tracer.record_trace("tx_abc", "ORDER_SERVICE", "EMIT_CREATED")
    tracer.record_trace("tx_abc", "INVENTORY_SERVICE", "CONSUME_AND_HOLD")
    
    path = tracer.extract_full_pipeline_path("tx_abc")
    assert path == ["ORDER_SERVICE->EMIT_CREATED", "INVENTORY_SERVICE->CONSUME_AND_HOLD"]