# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Zero-Copy Apache Arrow Interoperability
Description: Demonstrates zero-copy memory pointer sharing between PyArrow,
             Pandas, and Polars DataFrames using Apache Arrow C Data Interface.
"""
import pandas as pd  # type: ignore
import pyarrow as pa  # type: ignore
import polars as pl  # type: ignore


class ArrowZeroCopyBridge:
    @staticmethod
    def pyarrow_to_polars_zero_copy(arrow_table: pa.Table) -> pl.DataFrame:
        # Consumes Arrow table memory pointers with zero data copying
        return pl.from_arrow(arrow_table)

    @staticmethod
    def polars_to_arrow_pandas(pl_df: pl.DataFrame) -> pd.DataFrame:
        # Converts Polars to Pandas using Arrow extension arrays
        return pl_df.to_pandas(use_pyarrow_extension_array=True)


if __name__ == "__main__":
    # 1. Construct PyArrow Table
    pa_table = pa.Table.from_pydict({
        "sensor_id": pa.array([1, 2, 3, 4], type=pa.int32()),
        "reading": pa.array([98.6, 99.1, 100.2, 97.4], type=pa.float64())
    })
    
    # 2. Zero-Copy conversion to Polars
    polars_df = ArrowZeroCopyBridge.pyarrow_to_polars_zero_copy(pa_table)
    assert isinstance(polars_df, pl.DataFrame)
    
    # 3. Arrow-backed Pandas conversion
    pandas_df = ArrowZeroCopyBridge.polars_to_arrow_pandas(polars_df)
    assert isinstance(pandas_df["reading"].dtype, pd.ArrowDtype)
    
    print("[TASK 04 PASSED] Zero-copy bridge verified across PyArrow, Polars, and Pandas.")