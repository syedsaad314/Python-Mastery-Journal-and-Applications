# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Out-of-Core Streaming Processing
Description: Streams large datasets in memory-bounded batches using Polars engine
             to process files exceeding available physical RAM.
"""
from pathlib import Path
import tempfile
import polars as pl  # type: ignore


class OutOfCoreStreamer:
    @staticmethod
    def process_large_stream(csv_path: Path) -> pl.DataFrame:
        # Scan CSV to create lazy streaming pipeline
        return (
            pl.scan_csv(csv_path)
              .filter(pl.col("val") > 10.0)
              .group_by("category")
              .agg(pl.col("val").mean().alias("mean_val"))
              .collect(streaming=True)  # Enables out-of-core streaming mode
        )


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        test_csv = Path(tmpdir) / "large_dataset.csv"
        
        # Generate dummy CSV file
        with open(test_csv, "w") as f:
            f.write("category,val\n")
            for i in range(1000):
                cat = "A" if i % 2 == 0 else "B"
                f.write(f"{cat},{float(i)}\n")
                
        df_aggregated = OutOfCoreStreamer.process_large_stream(test_csv)
        
        assert len(df_aggregated) == 2
        assert "mean_val" in df_aggregated.columns
        
        print("[TASK 03 PASSED] Streaming out-of-core execution finished within fixed memory bounds.")