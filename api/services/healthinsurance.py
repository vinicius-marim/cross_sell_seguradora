import pickle
import pandas as pd
import inflection
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, TargetEncoder, OrdinalEncoder
from lightgbm import LGBMClassifier as LGBM


class HealthInsurance:

    def __init__( self ):
        self.trained_model   = pickle.load( open( 'api/lgbm(86.6).pkl', 'rb' ) )


    def rename_columns(self, dataset):

        # Modificação nomes colunas
        snakecase = lambda x : inflection.underscore( x )
        dataset.columns = list( map( snakecase, dataset.columns ) )

        return dataset

    def feature_creation_selection(self, dataset):

        # Feature Creation
        dataset['age_group'] = pd.cut(dataset['age'], bins=13, labels=False)
        dataset['vintage_group'] = pd.cut(dataset['vintage'], bins=100, labels=False )

        # Feature Selection
        selected_features = ['annual_premium', 'age', 'vintage', 'region_code', 'vintage_group', 
                             'policy_sales_channel', 'vehicle_damage', 'age_group', 'previously_insured', 
                             'gender', 'vehicle_age']

        df = dataset[selected_features]

        return df


    def get_prediction(self, original_data, test_data):

        prediction = self.trained_model.predict_proba( test_data )

        original_data['score'] = prediction[:, 1].tolist()


        def categoriza(x):
            var = ''
            if x> 0.80:
                var = 'Muito Alta' 
            elif 0.80 >= x >0.60:
                var = 'Alta'
            elif 0.60 >= x >0.40:
                var = 'Médio' 
            else:
                var = 'Baixo'
            return var

        original_data['propensão'] = original_data['score'].apply(categoriza)

        return original_data

    
def predict_process(data):

    # Criar o pipeline e fazer a previsão
    health_pipeline = HealthInsurance()

    df1 = health_pipeline.rename_columns(data)
    df2 = health_pipeline.feature_creation_selection(df1)

    print('Iniciando cálculos de previsões')

    df_response = health_pipeline.get_prediction(df, df2)

    # Preparar dados para escrita
    df_response.fillna('', inplace=True)  # Substituir NaN por string vazia para evitar erros

    df_update = pd.concat([df1['id'], df_response[['score', 'propensão']]], axis=1)
    print('Previsões prontas para serem lançadas')

    return df_update
