import os
import pandas as pd
from optbinning import BinningProcess

'''
conda create --name optbinning
pip install optbinning
'''

# Oppen Dataset
DIR_PATH = os.path.join(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'model'), 'data')
dataset = pd.read_csv(os.path.join(DIR_PATH, 'customer_data.csv'))


# Defining Variables Columns
ident_cols = ['id', 'date', 'label']
y_col= 'label'
X_cols = [col for col in dataset.columns if col not in ident_cols]


X = dataset[X_cols]
y = dataset[y_col].values
id = dataset[ident_cols]


optb = BinningProcess(variable_names=X_cols)
optb.fit(X, y)

tb_iv = optb.summary()
tb_iv.sort_values(by='iv', ascending=False)



'''
Source: http://gnpalencia.org/optbinning/binning_process.html
'''