from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("SimpleETLJob").getOrCreate()

    df = spark.read.csv("./datasets/sample_data.csv", header=True, inferSchema=True)
    filtered = df.filter("value > 10")

    filtered.write.mode("overwrite").csv("./output/")
    print("ETL job complete. Output written to ./output/")
    spark.stop()
    
if __name__ == "__main__":
    main()
