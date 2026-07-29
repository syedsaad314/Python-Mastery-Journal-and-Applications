# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Memory-Bounded Out-Of-Core Parquet Streaming
Description: Scans and aggregates massive Parquet datasets while strictly limiting
             DuckDB RAM usage to process datasets larger than memory.
"""
from pathlib import Path
import tempfile
import duckdb  # type: ignore
import pyarrow as pa  # type: ignore
import pyarrow.parquet as pq  # type: ignore


class OutOfCoreParquetScanner:
    @staticmethod
    def stream_parquet_aggregation(file_path: Path, max_memory_mb: int) -> float:
        conn = duckdb.connect(database=":memory:")
        # Limit memory footprint to demonstrate out-of-core spilling
        conn.execute(f"SET max_memory='{max_memory_mb}MB';")
        
        query = f"SELECT AVG(metric_val) FROM read_parquet('{file_path.as_posix()}');"
        result = conn.execute(query).fetchone()
        return float(result[0]) if result else 0.0


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "large_metrics.parquet"
        
        # Write dummy Parquet file via PyArrow
        table = pa.Table.from_pydict({
            "metric_val": pa.array([float(i) for i in range(1, 1001)], type=pa.float64())
        })
        pq.write_table(table, parquet_file)
        
        avg_val = OutOfCoreParquetScanner.stream_parquet_aggregation(parquet_file, max_memory_mb=16)
        
        expected_avg = (1000 + 1) / 2.0
        assert abs(avg_val - expected_avg) < 1e-5
        
        print(f"[TASK 03 PASSED] DuckDB out-of-core Parquet scan calculated metric mean: {avg_val:.2f}")