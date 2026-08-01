# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Parallel Multi-Threaded Hash GroupBy Aggregations
Description: Demonstrates parallelized hash partitioning and aggregate evaluations 
             across multiple CPU cores using Polars expression context.
"""
import polars as pl  # type: ignore


class ParallelAggregationEngine:
    @staticmethod
    def compute_group_metrics(df: pl.DataFrame) -> pl.DataFrame:
        return (
            df.group_by("department")
            .agg([
                pl.col("salary").mean().alias("avg_salary"),
                pl.col("salary").max().alias("max_salary"),
                pl.col("employee_id").count().alias("headcount")
            ])
            .sort("department")
        )


if __name__ == "__main__":
    data = pl.DataFrame({
        "department": ["Eng", "Eng", "HR", "Eng", "HR"],
        "employee_id": [1, 2, 3, 4, 5],
        "salary": [100000.0, 120000.0, 80000.0, 110000.0, 85000.0]
    })

    res = ParallelAggregationEngine.compute_group_metrics(data)

    assert len(res) == 2
    eng_row = res.filter(pl.col("department") == "Eng")
    assert eng_row["headcount"][0] == 3
    assert abs(eng_row["avg_salary"][0] - 110000.0) < 1e-5

    print("[TASK 04 PASSED] Multi-threaded GroupBy aggregation computed successfully.")