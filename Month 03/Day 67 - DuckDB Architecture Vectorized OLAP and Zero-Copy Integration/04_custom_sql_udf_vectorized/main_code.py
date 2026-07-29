# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Vectorized Python User-Defined Functions (UDFs)
Description: Registers vectorized Python scalar functions into DuckDB for high-throughput
             batch function evaluation using PyArrow/NumPy arrays.
"""
import duckdb  # type: ignore
import numpy as np  # type: ignore


class VectorizedUDFEngine:
    @staticmethod
    def calculate_tax_vectorized(amount_array):
        # Operates natively on NumPy/PyArrow vector batches
        return amount_array * 0.15

    @classmethod
    def register_and_execute(cls) -> list:
        conn = duckdb.connect(database=":memory:")
        
        # Register function using vector input/output types
        conn.create_function(
            "calculate_tax", 
            cls.calculate_tax_vectorized, 
            [duckdb.typing.DOUBLE], 
            duckdb.typing.DOUBLE,
            type="arrow"
        )
        
        query = "SELECT calculate_tax(100.0) AS tax_a, calculate_tax(200.0) AS tax_b;"
        return conn.execute(query).fetchall()


if __name__ == "__main__":
    results = VectorizedUDFEngine.register_and_execute()
    tax_a, tax_b = results[0]
    
    assert abs(tax_a - 15.0) < 1e-5
    assert abs(tax_b - 30.0) < 1e-5
    
    print(f"[TASK 04 PASSED] Vectorized Arrow UDF evaluated in DuckDB: Tax A={tax_a}, Tax B={tax_b}")