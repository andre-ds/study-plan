import pandas as pd


def dataset_description(dataset):
    
    dataset = pd.DataFrame({'Tipo': dataset.dtypes,
                    'Quantidade_Nan': dataset.isna().sum(),
                    'Percentual_Nan': (dataset.isna().sum() / dataset.shape[0]) * 100,
                    'Valores_Unicos': dataset.nunique()})
    return dataset