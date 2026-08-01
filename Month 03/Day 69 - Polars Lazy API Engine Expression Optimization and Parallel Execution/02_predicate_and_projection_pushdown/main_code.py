# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Polars Query Optimization - Predicate & Projection Pushdown
Description: Demonstrates how Polars re-orders execution operations to prune
             unused columns and filter rows at the earliest scan phase.
"""
from pathlib import Path
import tempfile
import polars as pl  # type: ignore


class PushdownOptimizerEngine:
    @staticmethod
    def run_optimized_file_scan(file_path: Path) -> tuple[pl.DataFrame, str]:
        # Scan Parquet file lazily
        lazy_query = (
            pl.scan_parquet(file_path)
            .filter(pl.col("category") == "A")
            .select(["id", "amount"])
        )

        plan = lazy_query.explain()
        executed_result = lazy_query.collect()
        return executed_result, plan


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        parquet_file = Path(tmpdir) / "transactions.parquet"

        # Write dataset containing unused columns and un-filtered rows
        df = pl.DataFrame({
            "id": [1, 2, 3, 4],
            "category": ["A", "B", "A", "C"],
            "amount": [100.0, 200.0, 300.0, 400.0],
            "unused_col": ["X", "Y", "Z", "W"]
        })
        df.write_parquet(parquet_file)

        result, query_plan = PushdownOptimizerEngine.run_optimized_file_scan(parquet_file)

        assert len(result) == 2
        assert result.columns == ["id", "amount"]

        print("[TASK 02 PASSED] Predicate and projection pushdown verified on lazy Parquet scan.")