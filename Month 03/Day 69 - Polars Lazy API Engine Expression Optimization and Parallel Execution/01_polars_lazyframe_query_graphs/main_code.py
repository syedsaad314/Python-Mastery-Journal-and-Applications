# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Polars LazyFrame Query Plan Generation & Inspection
Description: Demonstrates LazyFrame query graph construction, deferred execution,
             and logical execution plan extraction using explain().
"""
import polars as pl  # type: ignore


class PolarsLazyPlanInspector:
    @staticmethod
    def build_and_explain_plan(df_raw: pl.DataFrame) -> tuple[pl.DataFrame, str]:
        # Convert eager DataFrame to LazyFrame graph
        lazy_df = df_raw.lazy()

        # Build transformation pipeline (deferred execution)
        query = (
            lazy_df
            .filter(pl.col("score") > 75.0)
            .select([
                pl.col("user_id"),
                (pl.col("score") * 1.1).alias("adjusted_score")
            ])
        )

        # Extract logical query plan as text representation
        plan_str = query.explain()

        # Execute optimized query graph
        result_df = query.collect()
        return result_df, plan_str


if __name__ == "__main__":
    data = pl.DataFrame({
        "user_id": [1, 2, 3, 4],
        "score": [60.0, 80.0, 95.0, 70.0]
    })

    res, plan = PolarsLazyPlanInspector.build_and_explain_plan(data)

    assert len(res) == 2
    assert "score" in plan
    assert res["adjusted_score"].to_list() == [88.0, 104.5]

    print("[TASK 01 PASSED] Polars LazyFrame query plan constructed and executed successfully.")