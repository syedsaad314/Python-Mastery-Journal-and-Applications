# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Tungsten Engine & Off-Heap Memory Configuration
Description: Demonstrates Spark Tungsten engine memory allocation configurations,
             enabling off-heap memory management and binary UnsafeRow formatting.
"""
from pyspark.sql import SparkSession  # type: ignore


class TungstenMemoryEngine:
    @staticmethod
    def configure_off_heap_spark() -> tuple:
        # Build Spark Session configured with Tungsten Off-Heap Memory settings
        spark = (
            SparkSession.builder
            .appName("Day70_TungstenMemory")
            .master("local[1]")
            .config("spark.memory.offHeap.enabled", "true")
            .config("spark.memory.offHeap.size", "64m")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        is_off_heap = spark.conf.get("spark.memory.offHeap.enabled")
        off_heap_size = spark.conf.get("spark.memory.offHeap.size")

        # Create DataFrame executing under Tungsten binary row layout
        df = spark.range(1, 100).selectExpr("id AS val_a", "id * 2 AS val_b")
        count = df.count()

        spark.stop()
        return is_off_heap, off_heap_size, count


if __name__ == "__main__":
    enabled, size, row_count = TungstenMemoryEngine.configure_off_heap_spark()

    assert enabled == "true"
    assert size == "64m"
    assert row_count == 99

    print(f"[TASK 03 PASSED] Tungsten engine configured with off-heap memory ({size}). Processed {row_count} rows.")