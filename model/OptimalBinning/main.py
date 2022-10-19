import os
import optbinning
import pandas as pd

'''
pip uninstall scipy
pip uninstall mlflow
pip uninstall numpy
pip install numpy==1.22.4
pip install optbinning


conda install optbinning

Packeges:
pip install optuna
pip install lightgbm -U
pip install yellowbrick
pip install pycaret
pip install xverse
pip install optbinning -U
pip install --upgrade numpy
pip install -U scikit-learn
'''
'''
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
ropwr 0.3.0 requires scipy>=1.6.1, but you have scipy 1.5.4 which is incompatible.
optuna 3.0.3 requires scipy<1.9.0,>=1.7.0, but you have scipy 1.5.4 which is incompatible.
optbinning 0.15.1 requires scipy>=1.6.0, but you have scipy 1.5.4 which is incompatible.
investpy 1.0.8 requires numpy>=1.21.2, but you have numpy 1.19.5 which is incompatible.
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


optb = BinningProcess(name=X_cols)
optb.fit(X, y)

tb_iv = binning_process.summary()
tb_iv.sort_values(by='iv', ascending=False)


'''
Source: http://gnpalencia.org/optbinning/index.html
'''