# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: PySpark DataFrame Logical & Physical Execution Plans
Description: Demonstrates DataFrame query plan compilation and execution plan 
             inspection using PySpark's Catalyst query engine (.explain()).
"""
from pyspark.sql import SparkSession  # type: ignore
from pyspark.sql import functions as F  # type: ignore


class PySparkPlanInspector:
    def __init__(self):
        self.spark = (
            SparkSession.builder
            .appName("Day70_PlanInspector")
            .master("local[1]")
            .getOrCreate()
        )
        self.spark.sparkContext.setLogLevel("ERROR")

    def inspect_execution_plan(self) -> tuple:
        df = self.spark.createDataFrame([
            (1, "Alice", 5000.0),
            (2, "Bob", 3000.0),
            (3, "Charlie", 7000.0)
        ], ["id", "name", "salary"])

        # Construct lazy transformation pipeline
        query = (
            df.filter(F.col("salary") > 3500.0)
              .select("id", "name", (F.col("salary") * 1.1).alias("adjusted_salary"))
        )

        # Capture physical execution plan text string
        extended_plan_str = query._jdf.queryExecution().explainString(self.spark._sc._jvm.org.apache.spark.sql.execution.Extended())
        results = query.collect()

        return results, extended_plan_str


if __name__ == "__main__":
    inspector = PySparkPlanInspector()
    records, plan_text = inspector.inspect_execution_plan()

    assert len(records) == 2
    assert "Filter" in plan_text or "Project" in plan_text

    print(f"[TASK 01 PASSED] PySpark DataFrame query compiled and executed on {len(records)} records.")
    inspector.spark.stop()