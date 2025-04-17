import unittest
from pyspark.sql import SparkSession

class TestETLJob(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local").appName("ETLTest").getOrCreate()
        cls.test_data = [
            (1, 5),
            (2, 15),
            (3, 25)
        ]
        cls.columns = ["id", "value"]

    def test_etl_filter(self):
        df = self.spark.createDataFrame(self.test_data, self.columns)
        result_df = df.filter("value > 10")
        results = result_df.collect()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(row['value'] > 10 for row in results))

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

if __name__ == "__main__":
    unittest.main()
