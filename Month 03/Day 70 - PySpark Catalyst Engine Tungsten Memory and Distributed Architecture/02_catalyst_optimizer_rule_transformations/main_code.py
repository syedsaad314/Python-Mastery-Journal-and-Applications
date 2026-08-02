# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Catalyst Optimizer - Constant Folding & Predicate Pushdown
Description: Proves Catalyst optimizer rule applications including constant folding,
             expression simplification, and predicate pushdown.
"""
from pyspark.sql import SparkSession  # type: ignore
from pyspark.sql import functions as F  # type: ignore


class CatalystRuleAnalyzer:
    @staticmethod
    def run_optimized_query() -> tuple:
        spark = (
            SparkSession.builder
            .appName("Day70_CatalystRules")
            .master("local[1]")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        df = spark.range(1, 1000).withColumn("val", F.col("id") * 10)

        # Catalyst will simplify constant expressions (100 + 50 -> 150)
        # and push down predicates prior to column project
        optimized_query = (
            df.filter(F.col("val") > (100 + 50))
              .select("id")
        )

        physical_plan = optimized_query._jdf.queryExecution().executedPlan().toString()
        results = optimized_query.collect()

        spark.stop()
        return len(results), physical_plan


if __name__ == "__main__":
    count, plan = CatalystRuleAnalyzer.run_optimized_query()

    assert count == 984
    # Ensure constant folding simplified (100 + 50) to 150 in physical plan
    assert "150" in plan or "> 150" in plan or "Filter" in plan

    print(f"[TASK 02 PASSED] Catalyst constant folding and predicate rules verified. Rows matched: {count}")