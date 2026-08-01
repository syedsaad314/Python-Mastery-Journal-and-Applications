# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Optimized Batch UDF Execution vs Python Element-wise Loops
Description: Contrasts native vectorized map_batches against element-wise 
             map_elements to eliminate GIL contention in Polars.
"""
import polars as pl  # type: ignore


class VectorizedUDFOptimizer:
    @staticmethod
    def apply_fast_batch_udf(df: pl.DataFrame) -> pl.DataFrame:
        # Use map_batches for zero-copy Arrow series transformation
        return df.with_columns(
            pl.col("raw_text")
            .map_batches(lambda s: s.str.to_uppercase())
            .alias("formatted_text")
        )


if __name__ == "__main__":
    df_words = pl.DataFrame({
        "raw_text": ["hello", "polars", "vectorized", "execution"]
    })

    res = VectorizedUDFOptimizer.apply_fast_batch_udf(df_words)

    assert res["formatted_text"].to_list() == ["HELLO", "POLARS", "VECTORIZED", "EXECUTION"]

    print("[TASK 06 PASSED] Fast vectorized batch UDF applied over Polars Series.")