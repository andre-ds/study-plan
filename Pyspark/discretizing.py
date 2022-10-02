from pyspark.ml.feature import Bucketizer
import numpy as np
from sklearn import datasets
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, isnan, when
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, percent_rank, ntile, lag


spark = SparkSession(SparkContext(conf=SparkConf())
                     .getOrCreate())


date = (("James", "Sales", 3000),
              ("Michael", "Sales", 4600),
              ("Robert", "Sales", 4100),
              ("Maria", "Finance", 3000),
              ("James", "Sales", 3000),
              ("Scott", "Finance", 3300),
              ("Jen", "Finance", 3900),
              ("Jeff", "Marketing", 3000),
              ("Kumar", "Marketing", 2000),
              ("Saif", "Sales", 4100)
              )

columns = ['employee_name', 'department', 'salary']
dataset = spark.createDataFrame(data=date, schema=columns)
dataset.show()

# Window
windowSpec = Window.partitionBy().orderBy('salary')

# row_number
dataset = dataset.withColumn('row_number', row_number().over(windowSpec))
dataset.show()

# percent_rank
dataset = dataset.withColumn('percent_rank', percent_rank().over(windowSpec))
dataset.show()

# ntile
dataset = dataset.withColumn('ntile', ntile(5).over(windowSpec))
dataset.show()


# Bucketizer
# Bucketizer is used to transform a column of continuous features to a column of feature buckets defining the values ranges:

bucketizer = Bucketizer(splits=[0, 2000, 1000, 3000, 4000, float('Inf')],
                        inputCol='salary', outputCol='buckets')
dataset = bucketizer.setHandleInvalid('keep').transform(dataset)
dataset.show()

# lag
dataset = dataset.withColumn('lag', lag('salary', 1).over(windowSpec))
dataset.show()

dataset = dataset.withColumn('lag', lag('salary', -1).over(windowSpec))
dataset.show()

# Sources:
# https://sparkbyexamples.com/pyspark/pyspark-window-functions/
# https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.Bucketizer.html
# https://stackoverflow.com/questions/46225587/how-to-bin-in-pyspark
