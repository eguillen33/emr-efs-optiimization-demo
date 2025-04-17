import unittest
from pyspark.sql import SparkSession
import os

class TestETLJob(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local").appName("TestETL").getOrCreate()
        cls.test_data = [
            (1, 5),
            (2, 15),
            (3, 25)
        ]
        cls.columns = ["id", "value"]

    def test_etl_filtering(self):
        df = self.spark.createDataFrame(self.test_data, self.columns)
        result = df.filter("value > 10").collect()
        self.assertEqual(len(result), 2)

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
