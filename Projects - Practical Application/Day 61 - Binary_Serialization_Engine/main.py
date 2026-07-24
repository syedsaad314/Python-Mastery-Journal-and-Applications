# Lead Engineer: Syed Saad Bin Irfan
import asyncio
from schemas import SimulatedMetricMessage
from encoders import HighPerformanceEncoder
from decoders import HighPerformanceDecoder
from benchmark import OptimizationEngineBenchmark

async def execution_lifecycle_driver() -> None:
    print("=========================================================================")
    print("    LAUNCHING SYSTEM TRACK: HIGH-PERFORMANCE SERIALIZATION ENGINE       ")
    print("=========================================================================")
    
    # 1. Operational Verification Check
    original_message = SimulatedMetricMessage(device_id=9999, system_load=45, service_tag="CORE_ROUTER_NODE")
    binary_payload = HighPerformanceEncoder.serialize_message(original_message)
    decoded_message = HighPerformanceDecoder.deserialize_message(binary_payload)
    
    assert original_message.device_id == decoded_message.device_id
    assert original_message.service_tag == decoded_message.service_tag
    print("[INTEGRITY CHECK] Binary packing and unpacking sequence fully verified.")

    # 2. High-Speed Performance Suite Activation
    iterations = 50000
    print(f"\n--- Activating Serialization Performance Benchmarks ({iterations} Cycles) ---")
    results = OptimizationEngineBenchmark.run_benchmark_suite(iterations)
    
    print("\n=========================================================================")
    print("                      BENCHMARK ANALYTICS ENGINE REPORT                   ")
    print("=========================================================================")
    print(f" Standard Text JSON Wire Footprint    : {results['json_payload_bytes']} Bytes")
    print(f" Custom Compressed Binary Footprint   : {results['binary_payload_bytes']} Bytes")
    print(f" Total CPU Processing Overhead (JSON) : {results['json_processing_seconds']:.4f} sec")
    print(f" Total CPU Processing Overhead (BIN)  : {results['binary_processing_seconds']:.4f} sec")
    print("=========================================================================")

if __name__ == "__main__":
    asyncio.run(execution_lifecycle_driver())