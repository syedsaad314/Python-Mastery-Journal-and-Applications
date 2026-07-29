# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Unified Cross-Engine Querying (Pandas + Polars + DuckDB)
Description: Joins a Pandas DataFrame and a Polars DataFrame seamlessly inside DuckDB SQL 
             without manually converting or serializing either dataset.
"""
import duckdb  # type: ignore
import pandas as pd  # type: ignore
import polars as pl  # type: ignore


class UnifiedEngineBridge:
    @staticmethod
    def join_pandas_and_polars(df_pandas: pd.DataFrame, df_polars: pl.DataFrame) -> pl.DataFrame:
        conn = duckdb.connect(database=":memory:")
        
        # DuckDB automatically inspects caller frame and registers in-memory DataFrames
        query = """
            SELECT 
                p.user_id,
                p.user_name,
                o.order_amount
            FROM df_pandas p
            INNER JOIN df_polars o ON p.user_id = o.user_id
            ORDER BY p.user_id;
        """
        return conn.execute(query).pl()  # Direct export to Polars DataFrame


if __name__ == "__main__":
    # Pandas DataFrame (User metadata)
    df_pd = pd.DataFrame({
        "user_id": [1, 2, 3],
        "user_name": ["Alice", "Bob", "Charlie"]
    })
    
    # Polars DataFrame (Order transactions)
    df_pl = pl.DataFrame({
        "user_id": [1, 2, 3],
        "order_amount": [250.0, 450.5, 120.0]
    })
    
    df_joined = UnifiedEngineBridge.join_pandas_and_polars(df_pd, df_pl)
    
    assert isinstance(df_joined, pl.DataFrame)
    assert len(df_joined) == 3
    assert df_joined["user_name"].to_list() == ["Alice", "Bob", "Charlie"]
    
    print(f"[TASK 06 PASSED] DuckDB seamlessly joined Pandas + Polars DataFrames:\n{df_joined}")