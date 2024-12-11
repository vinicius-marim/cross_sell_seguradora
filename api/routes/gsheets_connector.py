import gspread
from google.oauth2.service_account import Credentials


class GsheetConnector:
    
    def __init__(self, service_account_file):
        self.client = gspread.service_account(service_account_file)


    def download_data(self, SHEET_ID, WORKSHEET_NAME):
        """Download do conteúdo do arquivo e da planilha informada.
        Esta Função retorna uma lista de dicionários para 
        ingestão do MLPipeline"""

        worksheet = self.client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
        # Carregar todos os dados como lista de dicionários
        data = worksheet.get_all_records()  
        return data


    def upload_data(self, SHEET_ID, WORKSHEET_NAME, update_content):
        """ Esta função envia dados(df_update) para 
        o arquivo e planilha informada"""
        
        # Salvar previsões no Sheets e Worksheet escolhido
        output_sheet = self.client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)
        # Limpar conteúdo do Worksheet selecionado (por segurança)
        output_sheet.clear()
        # Atualizar planilha com os novos dados
        output_sheet.update('A1', update_content)

        return None

