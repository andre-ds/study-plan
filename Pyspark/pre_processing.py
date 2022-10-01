import os
from datetime import date, datetime
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, sum, min, max, mean, isnan, when
#from pyspark.sql.functions import col, quarter, to_date, month, year, when, to_date, asc, months_between, round, concat, lit, regexp_replace, sum, max
from pyspark.sql.types import StructField, StructType, DateType, DoubleType, StringType, IntegerType, FloatType


spark = SparkSession(SparkContext(conf=SparkConf())
                     .getOrCreate())

# Datasize Source
# https://www.kaggle.com/datasets/praveengovi/credit-risk-classification-dataset?select=customer_data.csv
DIR_PATH = os.path.join(os.path.join(os.path.dirname(
    os.path.realpath('__file__')), 'Pyspark'), 'data')

# Oppen Dataset
dataset = spark.read.options(inferSchema='True', header='True').csv(
    os.path.join(DIR_PATH, 'customer_data.csv'))


# Missing Values
def missing_value_pct(dataset: DataFrame, type: dict):
    '''
    Test:
    missing_variables = missing_value_pct(dataset=dataset, type='dict')
    missing_variables

    missing_variables = missing_value_pct(dataset=dataset, type='spark_df')
    missing_variables.show()

    missing_variables = missing_value_pct(dataset=dataset, type='pandas_df')
    missing_variables.head()
    '''

    from pyspark.sql.functions import col, isnan, when, count
    total = dataset.count()

    if type == 'dict':
        missing_variables = {col: dataset.filter(isnan(
            dataset[col]) | dataset[col].isNull()).count()/total for col in dataset.columns}
        return missing_variables
    elif type == 'spark_df':
        missing_variables = dataset.select(
            [(count(when(isnan(c) | col(c).isNull(), c))/total).alias(c) for c in dataset.columns])
        return missing_variables
    elif type == 'pandas_df':
        import pandas as pd
        missing_variables = {col: dataset.filter(isnan(
            dataset[col]) | dataset[col].isNull()).count()/total for col in dataset.columns}
        missing_variables = pd.DataFrame.from_dict(
            missing_variables, orient='index').reset_index()
        missing_variables.columns = ['variable', 'pct']
        return missing_variables


missing_variables = missing_value_pct(dataset=dataset, type='dict')
missing_variables


# Removing Missing Values

# Selecting Variable by pct Missing Value Criteria
def remove_na_variables_from_dict(limit_list):
    import re

    result = {}
    for limit in limit_list:
        variable_list = [
            var for var in dataset.columns if missing_variables[var] > limit]
        for var in variable_list:
            limit = re.sub('[.]', '_', str(limit))
            result[f'X_limit_na_{limit}'] = variable_list

    return result


limit_list = [0.01, 0.02, 0.05, 0.2]
x_variabes_out_nan = remove_na_variables_from_dict(limit_list=limit_list)


dataset.show()
dataset.columns
dataset.printSchema()

schema = StructType([
    StructField('variable', StringType(), True),
    StructField('pct', FloatType(), True)])

missing_variables = spark.createDataFrame(
    data=missing_variables, schema=schema)
