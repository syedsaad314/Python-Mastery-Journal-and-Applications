# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Polars Expression Engine & Columnar Vectorization
Description: Demonstrates composing complex vectorized column expressions
             that execute natively in Rust without invoking Python callbacks.
"""
import polars as pl  # type: ignore


class PolarsExpressionEngine:
    @staticmethod
    def evaluate_complex_expression(df: pl.DataFrame) -> pl.DataFrame:
        # Parallelized multi-column expression evaluation
        return df.select([
            pl.col("id"),
            pl.when(pl.col("status") == "active")
              .then(pl.col("base_price") * (1.0 - pl.col("discount")))
              .otherwise(pl.col("base_price"))
              .alias("final_price")
        ])


if __name__ == "__main__":
    df_sample = pl.DataFrame({
        "id": [101, 102, 103],
        "status": ["active", "inactive", "active"],
        "base_price": [100.0, 50.0, 200.0],
        "discount": [0.10, 0.20, 0.15]
    })

    res = PolarsExpressionEngine.evaluate_complex_expression(df_sample)

    assert res["final_price"].to_list() == [90.0, 50.0, 170.0]

    print("[TASK 03 PASSED] Vectorized Polars expression tree computed in-memory.")