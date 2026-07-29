# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Copy Querying of Apache Arrow Tables via DuckDB
Description: Queries Apache Arrow memory buffers natively via DuckDB SQL engine
             without copying underlying data bytes into DuckDB storage.
"""
import duckdb  # type: ignore
import pyarrow as pa  # type: ignore


class ZeroCopyDuckDBBridge:
    @staticmethod
    def query_arrow_table(arrow_table: pa.Table, min_amount: float) -> pa.Table:
        # Register and query Arrow table zero-copy via DuckDB relation engine
        rel = duckdb.arrow(arrow_table)
        filtered_rel = rel.filter(f"amount >= {min_amount}").order("transaction_id")
        return filtered_rel.arrow()


if __name__ == "__main__":
    # Create Arrow Memory Table
    data = {
        "transaction_id": pa.array([1001, 1002, 1003, 1004], type=pa.int64()),
        "amount": pa.array([250.50, 12.00, 890.10, 45.00], type=pa.float64())
    }
    arrow_table = pa.Table.from_pydict(data)
    
    # Execute Zero-Copy SQL Query over Arrow Table
    result_arrow = ZeroCopyDuckDBBridge.query_arrow_table(arrow_table, min_amount=100.0)
    
    assert len(result_arrow) == 2
    assert result_arrow["transaction_id"].to_pylist() == [1001, 1003]
    
    print("[TASK 02 PASSED] DuckDB queried PyArrow table zero-copy and returned filtered Arrow Table.")