# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Spark Shuffle Engine, Partition Tuning, & Disk Spill
Description: Measures partition counts across wide transformation boundaries (joins/groupBy)
             and configures shuffle repartition limits.
"""
from pyspark.sql import SparkSession  # type: ignore


class ShufflePartitionEngine:
    @staticmethod
    def execute_shuffle_groupby(custom_partitions: int) -> tuple:
        spark = (
            SparkSession.builder
            .appName("Day70_ShuffleEngine")
            .master("local[2]")
            .config("spark.sql.shuffle.partitions", str(custom_partitions))
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("ERROR")

        # Seed multi-partition DataFrame
        df = spark.range(1, 10000, 1, numPartitions=4)
        
        # Wide transformation (Shuffle boundary)
        shuffled_df = df.groupBy((df.id % 5).alias("group_key")).count()
        
        actual_shuffle_partitions = shuffled_df.rdd.getNumPartitions()
        results = shuffled_df.collect()

        spark.stop()
        return actual_shuffle_partitions, len(results)


if __name__ == "__main__":
    shuffle_parts, group_count = ShufflePartitionEngine.execute_shuffle_groupby(custom_partitions=8)

    assert shuffle_parts == 8
    assert group_count == 5

    print(f"[TASK 04 PASSED] Wide shuffle transformation completed across {shuffle_parts} custom shuffle partitions.")