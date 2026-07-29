# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: DuckDB In-Memory Vectorized Query Execution
Description: Demonstrates DuckDB's vectorized query processing engine, evaluating
             vector chunks in CPU cache rather than row-by-row tuple evaluation.
"""
import duckdb  # type: ignore
import numpy as np  # type: ignore


class DuckDBVectorizedEngine:
    def __init__(self):
        self.conn = duckdb.connect(database=":memory:")

    def execute_vectorized_query(self, size: int) -> list:
        # Seed in-memory sequence table
        self.conn.execute(f"CREATE TABLE sensor_data AS SELECT range AS id, random() * 100 AS val FROM range({size});")
        
        # Execute vectorized filtered aggregation query
        query = """
            SELECT 
                COUNT(*) AS total_count, 
                AVG(val) AS avg_value 
            FROM sensor_data 
            WHERE val > 50.0;
        """
        return self.conn.execute(query).fetchall()


if __name__ == "__main__":
    engine = DuckDBVectorizedEngine()
    result = engine.execute_vectorized_query(10000)
    
    total_count, avg_val = result[0]
    
    assert total_count > 0
    assert 45.0 <= avg_val <= 55.0
    
    print(f"[TASK 01 PASSED] DuckDB Vectorized Engine executed query on 10,000 records. Result: Count={total_count}, Avg={avg_val:.2f}")