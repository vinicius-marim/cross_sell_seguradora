import joblib
import pandas as pd
import inflection

class MLPipeline:

    def __init__( self ):
        self.trained_model = joblib.load( open( 'models/lgbm(86.1).joblib', 'rb' ) )


    def rename_columns(self, dataset):

        # Modificação nomes colunas
        snakecase = lambda x : inflection.underscore( x )
        dataset.columns = list( map( snakecase, dataset.columns ) )

        return dataset

    def feature_creation_selection(self, dataset):

        # Feature Creation
        dataset['age_group'] = pd.cut(dataset['age'], bins=13, labels=False)

        # Feature Selection
        selected_features = ['annual_premium', 'age', 'vintage', 'region_code', 'driving_license', 
                             'policy_sales_channel', 'vehicle_damage', 'age_group', 'previously_insured', 
                             'gender', 'vehicle_age']

        return dataset[selected_features]


    def get_prediction(self, source_data, ML_prep_data):

        prediction = self.trained_model.predict_proba( ML_prep_data )

        source_data['score'] = prediction[:, 1].tolist()


        def propensity_level(x):
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

        source_data['propensão'] = source_data['score'].apply(propensity_level)

        return source_data

    
def full_predict_process(data):

    df = pd.DataFrame(data)

    # Criar o pipeline e fazer a previsão
    pipeline = MLPipeline()

    df1 = pipeline.rename_columns(df)
    df2 = pipeline.feature_creation_selection(df1)

    df_response = pipeline.get_prediction(df, df2)

    # Preparar dados para escrita
    df_response.fillna('', inplace=True)  # Substituir NaN por string vazia para evitar erros

    df_update = pd.concat([df1['id'], df_response[['score', 'propensão']]], axis=1)

    # Conversão para compatibilidade com GSheet API
    update_content = [df_update.columns.tolist()] + df_update.values.tolist()

    return update_content
