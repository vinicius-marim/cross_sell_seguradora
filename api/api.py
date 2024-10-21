import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from flask import Flask, request, jsonify, render_template
from healthinsurance import HealthInsurance

app = Flask(__name__)

# Configurar acesso ao Google Sheets usando service_account
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = '/Users/vinicius/1-Workstation/1-Repos_CDS/99-Misc/creds_pass/serv_key.json'

# creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.service_account(SERVICE_ACCOUNT_FILE)

# ID e nome da planilha do CRM
SHEET_ID = '1fGcpQ5pCB9pwbYSvMSlK-dLgj_r-1JnUO6eQO5Muurk'
WORKSHEET_NAME = 'CRM'

# ID e nome da planilha para salvar as previsões
OUTPUT_SHEET_ID = '1fGcpQ5pCB9pwbYSvMSlK-dLgj_r-1JnUO6eQO5Muurk'
OUTPUT_WORKSHEET_NAME = 'previsão'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def health_insurance_predict():
    try:
        # Conectar ao Google Sheets e carregar os dados do CRM
        sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
        print('Conectado ao CRM')
        data = sheet.get_all_records()  # Carregar todos os dados como lista de dicionários
        df = pd.DataFrame(data)  # Converter para DataFrame

        # Verificar se o DataFrame está vazio
        if df.empty:
            return jsonify({"message": "Nenhum dado encontrado na planilha do CRM."}), 400

        # Criar o pipeline e fazer a previsão
        health_pipeline = HealthInsurance()
        df1 = health_pipeline.rename_columns(df)
        df2 = health_pipeline.feature_selection(df1)
        print('Iniciando cálculos de previsões')
        df_response = health_pipeline.get_prediction(df, df2)

        # Salvar previsões de volta no Google Sheets de saída
        output_sheet = client.open_by_key(OUTPUT_SHEET_ID).worksheet(OUTPUT_WORKSHEET_NAME)
        # Limpar conteúdo anterior (opcional)
        output_sheet.clear()

        # Preparar dados para escrita
        df_response.fillna('', inplace=True)  # Substituir NaN por string vazia para evitar erros

        df_final = pd.concat([df1['id_cliente'], df_response[['score', 'nivel']]], axis=1)
        print('Lançando as previsões na planilha')

        # Atualizar planilha com os novos dados
        output_sheet.update([df_final.columns.values.tolist()] + df_final.values.tolist())

        return jsonify({"message": "Previsões realizadas e planilhas atualizadas com sucesso."}), 200

    except Exception as e:
        return jsonify({"message": f"Ocorreu um erro: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
