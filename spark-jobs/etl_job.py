# spark-jobs/etl_job.py

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ETLDemo").getOrCreate()

df = spark.read.csv("s3://your-bucket/sample_data.csv", header=True, inferSchema=True)
df_filtered = df.filter("value > 10")
df_filtered.write.mode("overwrite").csv("s3://your-bucket/output/")

spark.stop()
