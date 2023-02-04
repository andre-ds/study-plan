import os
import optuna
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, brier_score_loss
from sklearn.model_selection import train_test_split


'''
Packeges:
conda install -c conda-forge optuna
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


# Define an objective function to be minimized.

# =============================================================================
# Random Forest
# =============================================================================
def objective(trial):
    
    # Invoke suggest methods of a Trial object to generate hyperparameters.
    regressor_name = trial.suggest_categorical('classifier', ['RandomForest', 'lightGBM'])
    if regressor_name == 'RandomForest':
        max_depth = trial.suggest_int(name='max_depth', low=2, high=5)
        max_leaf_nodes = trial.suggest_int(name='max_leaf_nodes', low=10, high=40)
        min_impurity_decrease = trial.suggest_float(name='impurity', low=0.0, high=1.0, step=0.1)
        min_samples_leaf = trial.suggest_int(name='min_samples_leaf', low=10, high=60)
        n_estimators =  trial.suggest_int(name='n_estimators', low=30, high=50)
        model = RandomForestClassifier(random_state=7, class_weight='balanced_subsample',
            max_depth=max_depth, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease,
            min_samples_leaf=min_samples_leaf, n_estimators=n_estimators)
    elif regressor_name == 'lightGBM':
        objective = trial.suggest_categorical('objective', ['binary'])
        n_jobs = trial.suggest_categorical('n_jobs', [-1])
        class_weight = trial.suggest_categorical('class_weight', ['balanced'])
        metric = trial.suggest_categorical('metric', ['binary_logloss', 'cress_entropy', 'auc', 'avarege_precision'])
        lambda_l1 = trial.suggest_float(name='impurity', low=0.0, high=1e-8, step=3)
        lambda_l2 = trial.suggest_float(name='impurity', low=0.0, high=1e-8, step=3)
        max_depth = trial.suggest_int(name='max_depth', low=2, high=10)
        n_estimators =  trial.suggest_int(name='n_estimators', low=5, high=150)
        min_child_samples = trial.suggest_int(name='min_child_samples', low=50, high=15000)
        model = lightgbm(random_state=7, objective=objective, n_jobs=n_jobs,
                        class_weight=class_weight, metric=metric, lambda_l1=lambda_l1,
                        lambda_l2=lambda_l2, max_depth=max_depth, n_estimators=n_estimators,
                        min_child_samples=min_child_samples)


    model.fit(X_train, y_train)
    pred = model.predict(X_train)
    '''
    metric = average_precision_score(y_train, pred)
    '''
    metric = brier_score_loss(y_train, pred)

    # An objective value linked with the Trial object.
    return metric  

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=3)

# Model with tuned hyperparameters
best_params = study.best_params
model = RandomForestClassifier(**best_params)


# =============================================================================
# Xgboost
# =============================================================================

def objective(trial):
    
    # Invoke suggest methods of a Trial object to generate hyperparameters.
    regressor_name = trial.suggest_categorical('classifier', ['XGBoost'])
    if regressor_name == 'XGBoost':
        max_depth = trial.suggest_int(name='max_depth', low=10, high=50)
        learning_rate = trial.suggest_float(name='learning_rate', low=0.0, high=1.0, step=0.05)
        booster = trial.suggest_categorical('booster', ['gbtree', 'dart'])
        min_split_loss = trial.suggest_int(name='min_split_loss', low=0, high=50, step=10) #gamma
        subsample = trial.suggest_float(name='subsample', low=0.0, high=1.0, step=0.1)
        colsample_bytree = trial.suggest_float(name='impurity', low=0.0, high=1.0, step=0.1)
        reg_lambda = trial.suggest_float(name='reg_lambda', low=0.0, high=1.0, step=0.05)
        reg_alpha = trial.suggest_float(name='reg_alpha', low=1, high=2.0, step=0.05)
        n_estimators =  trial.suggest_int(name='n_estimators', low=30, high=50)
        model = xgb.XGBClassifier(random_state=7, objective='binary:logistic', max_depth=max_depth, learning_rate=learning_rate,
        booster=booster, min_split_loss=min_split_loss, subsample=subsample, colsample_bytree=colsample_bytree, reg_lambda=reg_lambda,
        reg_alpha=reg_alpha, n_estimators=n_estimators)

    model.fit(X_train, y_train)
    pred = model.predict(X_train)
    metric = average_precision_score(y_train, pred)

    # An objective value linked with the Trial object.
    return metric 

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=3)

# Model with tuned hyperparameters
best_params = study.best_params
model = xgb.XGBClassifier(**best_params)


'''
Source:
https://optuna.readthedocs.io/en/stable/index.html
https://scikit-learn.org/stable/modules/model_evaluation.html
https://xgboost.readthedocs.io/en/stable/parameter.html#additional-parameters-for-dart-booster-booster-dart
'''