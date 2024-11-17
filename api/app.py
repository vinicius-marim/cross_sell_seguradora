import os
from flask import Flask, request, jsonify, render_template
from services.ml_pipeline import full_predict_process
from routes.gsheets_connector import GsheetConnector
from dotenv import load_dotenv

load_dotenv()

AUTH = os.getenv("SERVICE_ACCOUNT_FILE")
# ID e nome da planilha do CRM
SHEET_ID = os.getenv("YOUR_SHEET_ID")
WORKSHEET_NAME = 'CRM'

# ID e nome da planilha para salvar as previsões
OUTPUT_SHEET_ID = os.getenv("YOUR_SHEET_ID")
OUTPUT_WORKSHEET_NAME = 'previsão'


templates_folder = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__,template_folder=templates_folder)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def health_insurance_predict():
    try:

        client = GsheetConnector(AUTH)
        data = client.download_data(SHEET_ID, WORKSHEET_NAME)

        predict_data = full_predict_process(data)

        upload_status = client.upload_data(OUTPUT_SHEET_ID, OUTPUT_WORKSHEET_NAME, predict_data)
        
        return jsonify({"status": "success", "message": "Dados enviados com sucesso", "details": str(upload_status)}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
