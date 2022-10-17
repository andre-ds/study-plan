import os
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier


def dataset_description(dataset):
    dataset = pd.DataFrame({'Tipo': dataset.dtypes,
                    'Quantidade_Nan': dataset.isna().sum(),
                    'Percentual_Nan': (dataset.isna().sum() / dataset.shape[0]) * 100,
                    'Valores_Unicos': dataset.nunique()})
    return dataset



# Oppen Dataset
DIR_PATH = os.path.join(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'model'), 'data')
dataset = pd.read_csv(os.path.join(DIR_PATH, 'customer_data.csv'))

# Detaset Basic Information
dataset_description(dataset=dataset)


# Defining Training and Out-of-time Dates
dataset['date'].unique()
out_of_time = ['2022-01', '2022-02', '2022-03']
training_dates = ['2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09']

# Creating Datasets
train = dataset[dataset['date'].isin(training_dates)]
out_of_time = dataset[dataset['date'].isin(out_of_time)]

# Defining Variables Columns
ident_cols = ['id', 'date', 'label']
y_col= 'label'
X_cols = [col for col in dataset.columns if col not in ident_cols]

# Train
X = train[X_cols]
y = train[y_col].values
id = train[ident_cols]

# Out-of-Time
X_out = out_of_time[X_cols]
y_out = out_of_time[y_col].values
dataset_out = out_of_time[ident_cols]


# Spliting Train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=7)


# Getting Index Rows
dataset_train = id.loc[X_train.index, :]
dataset_test = id.loc[X_test.index, :]


# Exemple Model
params = {'class_weight': 'balanced_subsample', 'max_depth': 40, 'max_leaf_nodes': 30, 'min_impurity_decrease': 0.0, 'min_samples_leaf': 50, 'n_estimators': 50, 'random_state': 7}
rnd = RandomForestClassifier(**params)
# Fitting
rnd.fit(X_train, y_train)


# Predictions
y_train_pred = rnd.predict(X_train)
y_train_prob = rnd.predict_proba(X_train)[:, 1]

y_test_pred = rnd.predict(X_test)
y_test_prob = rnd.predict_proba(X_test)[:, 1]

y_out_pred = rnd.predict(X_out)
y_out_prob = rnd.predict_proba(X_out)[:, 1]


# Creating Datasets with Predictions
dataset_train['prediction'] = y_train_pred
dataset_train['prob'] = y_train_prob

dataset_test['prediction'] = y_test_pred
dataset_test['prob'] = y_test_prob

dataset_out['prediction'] = y_out_pred
dataset_out['prob'] = y_out_prob
