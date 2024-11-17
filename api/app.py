import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from flask import Flask, request, jsonify, render_template
from healthinsurance import HealthInsurance
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = gspread.service_account(os.getenv("SERVICE_ACCOUNT_FILE"))

# ID e nome da planilha do CRM
SHEET_ID = os.getenv("YOUR_SHEET_ID")
WORKSHEET_NAME = 'CRM'

# ID e nome da planilha para salvar as previsões
OUTPUT_SHEET_ID = os.getenv("YOUR_SHEET_ID")
OUTPUT_WORKSHEET_NAME = 'previsão'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def health_insurance_predict():
    # try:
    # Conectar ao Google Sheets e carregar os dados do CRM
    sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
    print('Conectado ao CRM')
    sheet_data = sheet.get_all_records()  # Carregar todos os dados como lista de dicionários
    df = pd.DataFrame(sheet_data)  # Converter para DataFrame

    # Verificar se o DataFrame está vazio
    if df.empty:
        return jsonify({"message": "Nenhum dado encontrado na planilha (ID) informada."}), 400

    # Criar o pipeline e fazer a previsão
    health_pipeline = HealthInsurance()

    df1 = health_pipeline.rename_columns(df)
    df2 = health_pipeline.feature_creation_selection(df1)

    print('Iniciando cálculos de previsões')

    df_response = health_pipeline.get_prediction(df, df2)

    # Preparar dados para escrita
    df_response.fillna('', inplace=True)  # Substituir NaN por string vazia para evitar erros

    df_update = pd.concat([df1['id'], df_response[['score', 'propensão']]], axis=1)
    print('Lançando as previsões na planilha')

    # Salvar previsões de volta no Google Sheets em novo Worksheet
    output_sheet = client.open_by_key(OUTPUT_SHEET_ID).worksheet(OUTPUT_WORKSHEET_NAME)

    # Limpar conteúdo da Worksheet selecionada (por segurança)
    output_sheet.clear()

    # Atualizar planilha com os novos dados
    output_sheet.update([df_update.columns.tolist()] + df_update.values.tolist())

    return jsonify({"message": "Previsões realizadas e planilhas atualizadas com sucesso."}), 200

    # except Exception as e:
        # return jsonify({"message": f"Ocorreu um erro: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
