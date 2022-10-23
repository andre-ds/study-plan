import numpy as np
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, isnan, when


spark = SparkSession(SparkContext(conf=SparkConf())
                     .getOrCreate())

data = [
    ('James', 'CA', np.NaN), ('Julia', '', None),
    ('Ram', None, 200.0), ('Ramya', 'NULL', np.NAN)
]
dataset = spark.createDataFrame(data, ['name', 'state', "number"])
dataset.show()

# Detecting Missing
dataset.filter(dataset['state'].isNull()).show()
dataset.filter(dataset['number'].isNull()).show()

dataset.filter(isnan(dataset['state'])).show()
dataset.filter(isnan(dataset['number'])).show()


## Couting
dataset.filter(dataset['state'].isNull()).count()
dataset.filter(isnan(dataset['number'])).count()


## Creating Dictionary
missing_variables = {col: dataset.filter(dataset[col].isNull()).count() for col in dataset.columns}
missing_variables

missing_variables = {col: dataset.filter(isnan(dataset[col])).count() for col in dataset.columns}
missing_variables

## Adding pct
total = dataset.count()
missing_variables = {col: dataset.filter(isnan(dataset[col]) | dataset[col].isNull()).count()/total for col in dataset.columns}
missing_variables


## Creating Spark Dataframe
missing_variables = dataset.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in dataset.columns])
missing_variables.show()


# Fill Missing Values
dataset.show()
# Replace all missing
dataset.fillna(value=0).show()

# Replace Numerical Variable
dataset.fillna(value=0, subset=['number']).show()

# Replace String Variable
dataset.fillna(value='replace', subset=['state']).show()
