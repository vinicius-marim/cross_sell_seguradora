import pickle
import os
import pandas as pd
from flask import Flask, request, Response
from healthinsurance import HealthInsurance
from sklearn.ensemble import GradientBoostingClassifier
from lightgbm import LGBMClassifier as LGBM

# loading model and encoders


app = Flask( __name__)

@app.route( '/' )
def hello():
    return '<p>Modelo de machine learning online</p>'

@app.route( '/predict', methods=['POST'])

def health_insurance_predict():
    test_json = request.get_json()

    if test_json: 
        if isinstance( test_json, dict ): # Retorno Único
            test_raw = pd.DataFrame( test_json, index=[0] )
        
        else: # Retorno Múltiplo
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
        
        # Instanciada a Classe Principal (Health Inssurance)
        health_pipeline = HealthInsurance()

        df1 = health_pipeline.columns_rename( test_raw )

        df_response = health_pipeline.get_prediction( test_raw, df1 )

        return df_response
    
    else:
        return Response( '{}', status=200, mimetype='aplication/json')
    
if __name__ == '__main__':
    app.run( host= '0.0.0.0', debug=True )