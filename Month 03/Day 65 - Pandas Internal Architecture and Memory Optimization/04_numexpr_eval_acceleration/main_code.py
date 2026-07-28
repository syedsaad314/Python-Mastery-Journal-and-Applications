# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Chunked Memory-Bounded Stream Ingestion
Description: Reads massive dataset streams using chunk iterators to aggregate
             metrics in fixed O(1) memory space without loading whole files.
"""
import io
import numpy as np # type: ignore
import pandas as pd # type: ignore


class StreamAggregationEngine:
    @staticmethod
    def compute_streaming_mean(csv_buffer: io.StringIO, chunk_size: int) -> float:
        csv_buffer.seek(0)
        chunk_iterator = pd.read_csv(csv_buffer, chunksize=chunk_size)
        
        total_sum = 0.0
        total_count = 0
        
        for chunk in chunk_iterator:
            total_sum += chunk["metric_val"].sum()
            total_count += len(chunk["metric_val"])
            
        return total_sum / total_count if total_count > 0 else 0.0


if __name__ == "__main__":
    # Simulate a multi-MB streaming CSV file in memory
    csv_data = "id,metric_val\n" + "\n".join([f"{i},{i * 2.5}" for i in range(1, 1001)])
    buffer = io.StringIO(csv_data)
    
    streaming_mean = StreamAggregationEngine.compute_streaming_mean(buffer, chunk_size=100)
    
    # Mathematical baseline check: mean of 1..1000 multiplied by 2.5
    expected_mean = ((1000 + 1) / 2.0) * 2.5
    assert abs(streaming_mean - expected_mean) < 1e-5
    
    print(f"[TASK 03 PASSED] Streaming chunk aggregation computed mean: {streaming_mean:.4f}")