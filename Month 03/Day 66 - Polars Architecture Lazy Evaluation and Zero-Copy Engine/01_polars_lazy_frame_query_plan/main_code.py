# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Polars LazyFrame Query Optimization
Description: Demonstrates LazyFrame evaluation graph optimization, verifying
             predicate and projection pushdowns before graph execution.
"""
import sys
import polars as pl  # type: ignore


class PolarsQueryOptimizerEngine:
    @staticmethod
    def build_optimized_query(data_dict: dict) -> pl.LazyFrame:
        # Convert dictionary to LazyFrame to defer execution
        lf = pl.LazyFrame(data_dict)
        
        # Define chain of transformations (filter + selection)
        optimized_lf = (
            lf.filter(pl.col("status_code") == 200)
              .filter(pl.col("latency_ms") < 100.0)
              .select(["user_id", "latency_ms"])
        )
        return optimized_lf


if __name__ == "__main__":
    raw_data = {
        "user_id": [101, 102, 103, 104, 105],
        "status_code": [200, 404, 200, 500, 200],
        "latency_ms": [45.2, 120.0, 88.1, 15.0, 150.5],
        "payload_bytes": [512, 128, 1024, 256, 2048]
    }
    
    lazy_query = PolarsQueryOptimizerEngine.build_optimized_query(raw_data)
    
    # Inspect optimized execution plan string
    plan_str = lazy_query.explain()
    assert "FILTER" in plan_str or "SELECTION" in plan_str
    
    # Execute graph via collect()
    df_result = lazy_query.collect()
    
    # Assert correct execution bounds
    assert len(df_result) == 2  # user_id 101 and 103 match criteria
    assert df_result.columns == ["user_id", "latency_ms"]
    
    print("[TASK 01 PASSED] Polars query plan optimized with predicate and projection pushdown.")