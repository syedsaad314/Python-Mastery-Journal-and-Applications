# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Polars Parallel Expression Engine
Description: Implements complex vectorized conditional logic without custom Python
             lambda functions or .apply() bottlenecks.
"""
import numpy as np  # type: ignore
import polars as pl  # type: ignore


class ParallelExpressionEngine:
    @staticmethod
    def categorize_traffic(df: pl.DataFrame) -> pl.DataFrame:
        # Construct expressions executed in parallel on Rust query engine
        return df.with_columns(
            pl.when(pl.col("latency_ms") < 50.0)
              .then(pl.lit("FAST"))
              .when(pl.col("latency_ms") < 150.0)
              .then(pl.lit("MODERATE"))
              .otherwise(pl.lit("SLOW"))
              .alias("performance_tier"),
            (pl.col("bytes_sent") / 1024.0).round(2).alias("kb_sent")
        )


if __name__ == "__main__":
    df_input = pl.DataFrame({
        "session_id": ["s1", "s2", "s3", "s4"],
        "latency_ms": [12.4, 98.6, 210.0, 45.0],
        "bytes_sent": [2048, 4096, 1024, 8192]
    })
    
    df_processed = ParallelExpressionEngine.categorize_traffic(df_input)
    
    tiers = df_processed["performance_tier"].to_list()
    kb_sent = df_processed["kb_sent"].to_list()
    
    assert tiers == ["FAST", "MODERATE", "SLOW", "FAST"]
    assert kb_sent == [2.0, 4.0, 1.0, 8.0]
    
    print("[TASK 02 PASSED] Vectorized parallel expressions evaluated successfully.")