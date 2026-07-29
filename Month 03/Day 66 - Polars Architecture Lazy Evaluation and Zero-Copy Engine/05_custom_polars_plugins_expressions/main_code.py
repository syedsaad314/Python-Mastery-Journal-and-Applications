# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Window Functions & Complex Groupwise Struct Expressions
Description: Uses Polars .over() window expressions to compute intra-group 
             statistics without changing original DataFrame dimensions.
"""
import polars as pl  # type: ignore


class WindowExpressionEngine:
    @staticmethod
    def compute_group_normalized_metrics(df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns([
            # Calculate group mean using window functions (.over)
            pl.col("score").mean().over("department").alias("dept_avg_score"),
            # Calculate deviation from department mean
            (pl.col("score") - pl.col("score").mean().over("department")).alias("dept_deviation")
        ])


if __name__ == "__main__":
    raw_df = pl.DataFrame({
        "employee_id": [1, 2, 3, 4, 5],
        "department": ["HR", "ENG", "ENG", "HR", "ENG"],
        "score": [80.0, 90.0, 95.0, 70.0, 85.0]
    })
    
    result_df = WindowExpressionEngine.compute_group_normalized_metrics(raw_df)
    
    # Assert window calculated outputs
    hr_avg = result_df.filter(pl.col("department") == "HR")["dept_avg_score"][0]
    eng_avg = result_df.filter(pl.col("department") == "ENG")["dept_avg_score"][0]
    
    assert hr_avg == 75.0
    assert eng_avg == 90.0
    
    print(f"[TASK 05 PASSED] Window expression pipeline computed correctly:\n{result_df}")