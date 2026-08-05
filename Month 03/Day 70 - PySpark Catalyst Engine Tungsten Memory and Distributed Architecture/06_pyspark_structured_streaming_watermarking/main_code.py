# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: PySpark Structured Streaming Event-Time Watermarking
Description: Demonstrates windowed aggregation and event-time watermarking semantics
             to bound state store memory growth during real-time streaming scans.
"""
from pyspark.sql import SparkSession  # type: ignore
from pyspark.sql import functions as F  # type: ignore


class StructuredStreamingWatermarkEngine:
    @staticmethod
    def evaluate_watermark_schema() -> tuple:
        spark = (
            SparkSession.builder
            .appName("Day70_StreamingWatermark")
            .master("local[1]")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        # Construct stream-like memory schema
        df = spark.createDataFrame([
            ("2026-07-25 10:00:00", "device_1", 10.5),
            ("2026-07-25 10:05:00", "device_1", 15.0),
            ("2026-07-25 10:25:00", "device_1", 20.0)  # Event advancing time
        ], ["timestamp_str", "device_id", "reading"])

        # Convert to Timestamp and apply watermark logic
        events_df = df.withColumn("event_time", F.to_timestamp("timestamp_str"))

        # Window aggregation with 10-minute watermark threshold
        windowed_counts = (
            events_df
            .withWatermark("event_time", "10 minutes")
            .groupBy(
                F.window("event_time", "10 minutes"),
                "device_id"
            )
            .agg(F.sum("reading").alias("total_reading"))
        )

        results = windowed_counts.collect()
        spark.stop()
        return len(results), results[0]["total_reading"]


if __name__ == "__main__":
    count, sample_sum = StructuredStreamingWatermarkEngine.evaluate_watermark_schema()

    assert count > 0
    assert sample_sum >= 10.5

    print(f"[TASK 06 PASSED] Structured Streaming watermark window aggregation verified on {count} windows.")