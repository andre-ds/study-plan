import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql

load_dotenv()
connection = create_engine(os.getenv('connection'))

query = '''
select *
from olist.orders
'''
dataset = pd.read_sql(con=connection, sql=query)


order_purchase_timestamp
dataset.columns

dataset.head()