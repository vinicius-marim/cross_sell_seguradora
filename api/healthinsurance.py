import pickle
import pandas as pd
from category_encoders import OneHotEncoder, TargetEncoder


class HealthInsurance:

    def __init__( self ):
        self.trained_model   = pickle.load( open( 'api/lgbm(83.6).pkl', 'rb' ) )


    def rename_columns(self, dataset):

        new_columns = ['id_cliente', 'gender', 'age', 'driving_license', 'region_code', 'previously_insured', 
       'vehicle_age', 'vehicle_damage', 'annual_premium','policy_sales_channel', 'vintage']
        dataset.columns = new_columns

        return dataset

    def feature_selection(self, dataset):

        df = dataset.drop(columns=['id_cliente', 'driving_license', 'gender'])
        df['vintage_group'] = pd.cut(df['vintage'], bins=100, labels=False )

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

        original_data['conversão'] = original_data['score'].apply(categoriza)

        return original_data
