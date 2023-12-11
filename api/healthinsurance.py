import pickle
import pandas as pd
from category_encoders import OneHotEncoder, TargetEncoder


class HealthInsurance:

    def __init__( self ):
        self.model_pipe   = pickle.load( open( 'stack_model.pkl', 'rb' ) )


    def columns_rename(dataset):

        # Modificação nomes colunas
        new_columns = ['id', 'gender', 'age', 'driving_license', 'region_code', 'previously_insured', 
       'vehicle_age', 'vehicle_damage', 'annual_premium','policy_sales_channel', 'vintage']

        dataset.columns = new_columns

        return dataset


    def get_prediction(self, original_data, test_data):

        prediction = self.model_pipe.predict_proba( test_data )

        original_data['score'] = prediction[:, 1].tolist()

        return original_data.to_json( orient='records', date_format='iso')