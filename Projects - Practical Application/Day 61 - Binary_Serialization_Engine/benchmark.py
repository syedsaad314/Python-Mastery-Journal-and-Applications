# Lead Engineer: Syed Saad Bin Irfan
import json
import time
from schemas import SimulatedMetricMessage
from encoders import HighPerformanceEncoder
from decoders import HighPerformanceDecoder

class OptimizationEngineBenchmark:
    @staticmethod
    def run_benchmark_suite(cycles: int) -> dict:
        msg = SimulatedMetricMessage(device_id=4096, system_load=78, service_tag="MERN_PROD_CLUSTER")
        json_data = {"device_id": 4096, "system_load": 78, "service_tag": "MERN_PROD_CLUSTER"}
        
        # 1. Evaluate JSON Execution Metrics
        t0 = time.perf_counter()
        for _ in range(cycles):
            encoded = json.dumps(json_data).encode('utf-8')
            _ = json.loads(encoded)
        json_time = time.perf_counter() - t0
        
        # 2. Evaluate Binary Codec Execution Metrics
        t1 = time.perf_counter()
        for _ in range(cycles):
            packed = HighPerformanceEncoder.serialize_message(msg)
            _ = HighPerformanceDecoder.deserialize_message(packed)
        binary_time = time.perf_counter() - t1
        
        return {
            "json_processing_seconds": json_time,
            "binary_processing_seconds": binary_time,
            "json_payload_bytes": len(json.dumps(json_data).encode('utf-8')),
            "binary_payload_bytes": len(HighPerformanceEncoder.serialize_message(msg))
        }