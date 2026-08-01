# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Memory-Bounded Out-Of-Core Streaming via Polars
Description: Processes large dataset query graphs in batch chunks using 
             streaming execution to enforce strict memory ceiling bounds.
"""
from pathlib import Path
import tempfile
import polars as pl  # type: ignore


class PolarsStreamingEngine:
    @staticmethod
    def process_streaming_aggregation(file_path: Path) -> pl.DataFrame:
        # Enforce streaming execution engine on lazy query graph
        return (
            pl.scan_parquet(file_path)
            .group_by("region")
            .agg(pl.col("sales").sum().alias("total_sales"))
            .collect(streaming=True)
        )


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        data_path = Path(tmpdir) / "regional_sales.parquet"

        # Seed data
        df = pl.DataFrame({
            "region": ["North", "South", "North", "East", "South"] * 100,
            "sales": [50.0, 30.0, 70.0, 20.0, 40.0] * 100
        })
        df.write_parquet(data_path)

        result = PolarsStreamingEngine.process_streaming_aggregation(data_path)

        assert len(result) == 3
        north_sales = result.filter(pl.col("region") == "North")["total_sales"][0]
        assert north_sales == 12000.0

        print("[TASK 05 PASSED] Out-of-core streaming LazyFrame query executed successfully.")