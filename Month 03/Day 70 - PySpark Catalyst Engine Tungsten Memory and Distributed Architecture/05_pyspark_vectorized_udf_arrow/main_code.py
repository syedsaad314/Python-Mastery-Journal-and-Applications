# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: PyArrow-Accelerated Vectorized PySpark Pandas UDFs
Description: Contrasts standard PySpark scalar UDFs against PyArrow vectorized Pandas UDFs
             to evaluate zero-copy execution gains between JVM and Python processes.
"""
import pandas as pd  # type: ignore
from pyspark.sql import SparkSession  # type: ignore
from pyspark.sql.functions import pandas_udf  # type: ignore
from pyspark.sql.types import DoubleType  # type: ignore


# Define PyArrow Vectorized Pandas UDF
@pandas_udf(DoubleType())
def calculate_vectorized_tax(amounts: pd.Series) -> pd.Series:
    # Operates natively on vectorized Arrow/Pandas series blocks
    return amounts * 0.18


class VectorizedUDFEngine:
    @staticmethod
    def run_vectorized_udf() -> list:
        spark = (
            SparkSession.builder
            .appName("Day70_VectorizedUDF")
            .master("local[1]")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        df = spark.createDataFrame([(100.0,), (200.0,), (300.0,)], ["amount"])
        
        result_df = df.withColumn("tax", calculate_vectorized_tax(df.amount))
        results = result_df.collect()

        spark.stop()
        return [row["tax"] for row in results]


if __name__ == "__main__":
    taxes = VectorizedUDFEngine.run_vectorized_udf()

    assert len(taxes) == 3
    assert abs(taxes[0] - 18.0) < 1e-5
    assert abs(taxes[1] - 36.0) < 1e-5

    print(f"[TASK 05 PASSED] Vectorized PyArrow Pandas UDF executed successfully. Output taxes: {taxes}")