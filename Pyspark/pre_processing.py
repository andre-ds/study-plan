import os
from itertools import groupby
from msilib import type_binary
from datetime import date, datetime
from tkinter import Variable
from pyspark.context import SparkContext
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.window import Window
from pyspark.sql.functions import col, count, sum, min, max, mean, isnan, when, ntile, lit, round, log
#from pyspark.sql.functions import col, quarter, to_date, month, year, when, to_date, asc, months_between, round, concat, lit, regexp_replace, sum, max
from pyspark.sql.types import StructField, StructType, DateType, DoubleType, StringType, IntegerType, FloatType


spark = SparkSession(SparkContext(conf=SparkConf())
                     .getOrCreate())



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


def remove_na_variables_from_dict(limit_list):
    import re

    result = {}
    for limit in limit_list:
        variable_list = [var for var in dataset.columns if missing_variables[var] > limit]   
        # adding
        limit = re.sub('[.]', '_', str(limit))
        result[f'x_limit_na_{limit}'] = variable_list

    return result


def discretizing_percentile(dataset, variable, ntile_value, quantity_category=True):


    def _quantity_categories(dataset, variable):
        dataset = dataset.groupBy(variable).agg(count(col(variable)).alias('quantity'))
        quantity = dataset.select(variable).count()

        return quantity

    
    def _discretizing(dataset, ntile_value, variable):

        cat_variable = f'cat_{variable}'
        dataset = dataset.withColumn('partitionBy', lit('partitionBy'))
        dataset = dataset.withColumn(cat_variable, ntile(ntile_value) \
            .over(Window.partitionBy('partitionBy') \
            .orderBy(variable))).drop('partitionBy')

        return dataset


    if quantity_category == True:
        quantity = _quantity_categories(dataset=dataset, variable=variable)
        if quantity > 10:
            dataset = _discretizing(dataset=dataset, ntile_value=ntile_value, variable=variable)
        else:
            print(f'{variable} is already a categorical variable.')
    else:
        dataset = _discretizing(dataset=dataset, ntile_value=ntile_value, variable=variable)
        
    return dataset


def credit_indicators(dataset, target, variable, aggregation):
        
    table = dataset.withColumn(target, when(col(target) == 1, 'event_c').otherwise('non_event_c')) \
        .groupBy(target, variable).agg(count(target).alias('Quantity')) \
        .groupby(variable).pivot(target).max('Quantity') \
        .fillna(subset=['event_c', 'non_event_c'], value=0) \
        .withColumn('event_l', round((col('event_c')/(col('event_c')+col('non_event_c'))*100), 2)) \
        .withColumn('non_event_l', round((col('non_event_c')/(col('event_c')+col('non_event_c'))*100), 2))

    col_event_tot = table.agg(sum('event_c')).collect()[0][0]
    col_non_event_tot = table.agg(sum('non_event_c')).collect()[0][0]

    table = table.withColumn('event_c', round((col('event_c')/col_event_tot)*100, 2)) \
        .withColumn('non_event_c', round((col('non_event_c')/col_non_event_tot)*100, 2)) \
        .withColumn('WOE', round(log(2.71, col('event_c')/col('non_event_c')), 3)) \
        .withColumn('IV', round((col('non_event_c') - col('event_c'))*col('WOE'), 3))

    # Aggregation
    if aggregation == True:
        table = table.agg(lit(variable).alias('variable'),
                round(sum(col('WOE')), 2).alias('WOE'),
                round(sum(col('IV')), 2).alias('IV'))

    return table


def calc_credit_indicators(dataset, target, variable_list, aggregation):

    schema = StructType([
        StructField('variable', StringType(), True),
        StructField('WOE', FloatType(), True),
        StructField('IV', FloatType(), True)
    ])

    table = spark.createDataFrame(data=spark.sparkContext.emptyRDD(),schema=schema)
    for v in variable_list:
        tb = credit_indicators(dataset=dataset, target=target, variable=v, aggregation=aggregation)
        table = table.union(tb)

    return table


# Datasize Source
# https://www.kaggle.com/datasets/praveengovi/credit-risk-classification-dataset?select=customer_data.csv
DIR_PATH = os.path.join(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'Pyspark'), 'data')


# Oppen Dataset
dataset = spark.read.options(inferSchema='True', header='True').csv(os.path.join(DIR_PATH, 'customer_data.csv'))


# Missing Values
missing_variables = missing_value_pct(dataset=dataset, type='dict')
missing_variables


# Removing Missing Values
## Selecting Variable by pct Missing Value Criteria
limit_list = [0.01, 0.02, 0.05, 0.2]
x_variabes_out_nan = remove_na_variables_from_dict(limit_list=limit_list)
x_variabes_out_nan

## Removing Variables with more than 0.2 of missing value
dataset = dataset.drop(*x_variabes_out_nan['x_limit_na_0_2'])


# Calculating WOEs
## Lockinf for categorial variables
target_cols = ['label', 'id']
x_cols = [col for col in dataset.columns if col not in target_cols]
for v in x_cols:
    dataset = discretizing_percentile(dataset=dataset, variable=v, ntile_value=5, quantity_category=True)

# Calculate Credit Indicators (WOE, IV)
x_cols = [col for col in dataset.columns if col not in target_cols]

tb_credit_indicators = calc_credit_indicators(dataset=dataset, target='label', variable_list=x_cols, aggregation=True)
tb_credit_indicators.show()


