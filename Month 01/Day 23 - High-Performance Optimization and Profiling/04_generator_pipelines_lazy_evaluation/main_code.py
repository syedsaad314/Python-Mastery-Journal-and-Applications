"""
Core Topic: Lazy-Evaluation Generator Pipelines
Description: Streams high-volume data vectors through memory-efficient generator paths.
Lead Engineer: Syed Saad Bin Irfan
"""

from typing import Generator

def transaction_source_stream(limit: int) -> Generator[str, None, None]:
    """Generates sequential raw data entries on-demand without memory buffering."""
    for record_index in range(1, limit + 1):
        yield f"TXN-ID-2026-{record_index},AMOUNT={record_index * 1.5},STATUS=SUCCESS"

def processing_filter_pipeline(stream: Generator[str, None, None]) -> Generator[float, None, None]:
    """Filters data records and extracts transactional numeric amounts on the fly."""
    for raw_string in stream:
        if "STATUS=SUCCESS" in raw_string:
            parts = raw_string.split(",")
            amount_value = float(parts[1].split("=")[1])
            yield amount_value

if __name__ == "__main__":
    total_records = 100000
    print(f"[STREAM PIPELINE] Starting lazy evaluation pipeline over {total_records} virtual objects...")
    
    source = transaction_source_stream(total_records)
    pipeline = processing_filter_pipeline(source)
    
    # Process items one-by-one to maintain an ultra-low memory footprint
    cumulative_sum = 0.0
    for single_amount in pipeline:
        cumulative_sum += single_amount
        
    print(f"[STREAM PIPELINE] Processing finalized cleanly. Calculated Pipeline Sum: {cumulative_sum}")