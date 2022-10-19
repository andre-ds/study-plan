import os
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from plot_metric.functions import BinaryClassification
import scikitplot as skplt

'''
pip install plot-metric
conda install -c conda-forge scikit-plot
'''

def dataset_description(dataset):
    
    dataset = pd.DataFrame({'Tipo': dataset.dtypes,
                    'Quantidade_Nan': dataset.isna().sum(),
                    'Percentual_Nan': (dataset.isna().sum() / dataset.shape[0]) * 100,
                    'Valores_Unicos': dataset.nunique()})
    return dataset


# Oppen Dataset
DIR_PATH = os.path.join(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'model'), 'data')
dataset = pd.read_csv(os.path.join(DIR_PATH, 'customer_data.csv'))
dataset = dataset.fillna(0)

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


# Prediction
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

# =============================================================================
# Analyzing Confusion Matrix
# =============================================================================

# Analyzing test dataset results
print(confusion_matrix(y_train, y_train_pred))
print(classification_report(y_train, y_train_pred))

# Analyzing test dataset results
print(confusion_matrix(y_test, y_test_pred))
print(classification_report(y_test, y_test_pred))

# Analyzing out-of-time dataset results
print(confusion_matrix(y_out, y_out_pred))
print(classification_report(y_out, y_out_pred))


# =============================================================================
# Plot ROC Curve
# =============================================================================
#from plot_metric.functions import BinaryClassification

# ROC-Train
bc = BinaryClassification(y_train, y_train_pred, labels=["Class 1", "Class 2"])
plt.figure(figsize=(5,5))
bc.plot_roc_curve(title='ROC-Train')
plt.show()

# ROC-Test
bc = BinaryClassification(y_test, y_test_pred, labels=["Class 1", "Class 2"])
plt.figure(figsize=(5,5))
bc.plot_roc_curve(title='ROC-Test')
plt.show()


# =============================================================================
# Plot Precision Recall Curve
# =============================================================================

# ROC-Train
bc = BinaryClassification(y_train, y_train_pred, labels=["Class 1", "Class 2"])
plt.figure(figsize=(5,5))
bc.plot_precision_recall_curve(title='Precision-Recall-Train')
plt.show()

# ROC-Test
bc = BinaryClassification(y_test, y_test_pred, labels=["Class 1", "Class 2"])
plt.figure(figsize=(5,5))
bc.plot_precision_recall_curve(title='Precision-Recall-Test')
plt.show()


# =============================================================================
# Plot KS Curve
# =============================================================================
# import scikitplot as skplt

# Train
skplt.metrics.plot_ks_statistic(y_train, rnd.predict_proba(X_train), title='KS-Train')
plt.show()

# Test
skplt.metrics.plot_ks_statistic(y_test, rnd.predict_proba(X_test), title='KS-Test')
plt.show()


# =============================================================================
# GHs Analisys
# =============================================================================

## Creating GHs
dataset_train['gh'] = pd.cut(dataset_train['prob'], bins=10, right=True, labels=[1,2,3,4,5,6,7,8,9,10])
dataset_test['gh'] = pd.cut(dataset_test['prob'], bins=10, right=True, labels=[1,2,3,4,5,6,7,8,9,10])
dataset_out['gh'] = pd.cut(dataset_out['prob'], bins=10, right=True, labels=[1,2,3,4,5,6,7,8,9,10])

## Basic GH Analisys
dataset_train.groupby(['gh'])[y_col].agg(['mean', 'count'])
dataset_test.groupby(['gh'])[y_col].agg(['mean', 'count'])
dataset_out.groupby(['gh'])[y_col].agg(['mean', 'count'])

## GH Graph Analisys
fig = plt.figure(figsize=(18,8))
sns.lineplot(data=dataset_train, x='date', y='label', hue='gh', ci=None)
sns.lineplot(data=dataset_train, x='date', y='label', ci=None, color='black', label='Mean', dashes=[(2,2)])
plt.grid(axis='y', linestyle='--')
plt.xlabel('Date')
plt.ylabel('% Default')
plt.title('GHs Train')
plt.legend(loc='upper center', bbox_to_anchor=(1.1,0.8), fancybox=True)
plt.show()




'''
Sources:
https://plot-metric.readthedocs.io/en/latest/#

'''