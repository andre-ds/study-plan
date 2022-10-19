import os
#import pycaret
import pandas as pd
from pycaret.classification import *
#from pycaret.classification import *

'''
conda install -c conda-forge pycaret
'''

# Oppen Dataset
DIR_PATH = os.path.join(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'model'), 'data')
dataset = pd.read_csv(os.path.join(DIR_PATH, 'customer_data.csv'))


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


# =============================================================================
# Pycaret
# =============================================================================

data = train.drop(columns=['id', 'date'])

exp_clf = setup(data = train,
                target = 'label',
                session_id=1,
                fold=4,
                fold_shuffle=True,
                numeric_imputation='zero',
                normalize=True,
                normalize_method='robust',
                remove_multicollinearity=True,
                multicollinearity_threshold=0.95,
                polynomial_features=True,
                polynomial_degree=2,
                trigonometry_features=True,
                feature_interaction=True,
                n_jobs=10,
                silent=True,
                html=False,
                log_experiment=False) 

# Comparing All Models
best_model = compare_models(n_select = 3)
print(best_model)

# List of models
models()

 # Create Model
clf = create_model('lightgbm', fold=5)


# Tune Model
tuned_clf = tune_model(clf, optimize='AUC')


# Create Model
dt = create_model('dt')


# =============================================================================
# Graphs
# =============================================================================

plot_model(tuned_clf, plot = 'parameter')

# Plot AUC
plot_model(tuned_clf, plot = 'auc')

# Precision-Recall Curve
plot_model(tuned_clf, plot = 'pr')

# Feature Importance Plot
plot_model(tuned_clf, plot='feature')

# Confusion Matrix
plot_model(tuned_clf, plot = 'confusion_matrix')


# =============================================================================
# Prediction
# =============================================================================

out_of_time = predict_model(tuned_clf, data=out_of_time)
out_of_time.head()

'''
Source:
https://pycaret.gitbook.io/docs/get-started/quickstart
https://pycaret.gitbook.io/docs/get-started/tutorials
https://github.com/pycaret/pycaret/blob/master/tutorials/Binary%20Classification%20Tutorial%20Level%20Beginner%20-%20%20CLF101.ipynb

'''