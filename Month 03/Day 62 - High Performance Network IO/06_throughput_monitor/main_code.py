# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Real-Time Network Throughput Monitor
Description: Computes low-latency bandwidth usage tracking metrics and data speed delivery rates.
"""
import time

class NetworkThroughputMonitor:
    def __init__(self):
        self.total_bytes_transferred = 0
        self.tracking_window_start = time.perf_counter()

    def record_network_io_event(self, block_byte_size: int) -> None:
        if block_byte_size < 0:
            raise ValueError("Data metric configurations cannot scale inside negative bounds.")
        self.total_bytes_transferred += block_byte_size

    def compile_bandwidth_metrics(self) -> dict:
        elapsed_seconds = time.perf_counter() - self.tracking_window_start
        if elapsed_seconds <= 0:
            elapsed_seconds = 1e-6
            
        megabytes_processed = self.total_bytes_transferred / (1024 * 1024)
        throughput_rate_mb_per_sec = megabytes_processed / elapsed_seconds
        
        return {
            "elapsed_seconds": round(elapsed_seconds, 4),
            "total_bytes_ingested": self.total_bytes_transferred,
            "throughput_mbps": round(throughput_rate_mb_per_sec, 2)
        }

if __name__ == "__main__":
    monitor = NetworkThroughputMonitor()
    # Simulating massive network ingest: 5MB packet arrival
    monitor.record_network_io_event(5 * 1024 * 1024)
    data_metrics = monitor.compile_bandwidth_metrics()
    assert data_metrics["total_bytes_ingested"] == 5242880
    assert data_metrics["throughput_mbps"] >= 0.0
    print(f"[TASK 06 PASSED] Live network bandwidth tracking audit completed: {data_metrics}")