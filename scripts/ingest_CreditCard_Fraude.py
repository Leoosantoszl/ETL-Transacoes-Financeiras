import os
import zipfile
import pandas as pd
from loguru import logger
# from kaggle.api.kaggle_api_extended import KaggleApi

# kaggle_json_path = os.path.expanduser('secrets/kaggle.json')
# os.environ['KAGGLE_CONFIG_DIR'] = os.path.abspath('secrets')

# # Inicializa a API
# api = KaggleApi()
# api.authenticate()
# Caminhos
KAGGLE_DATASET = "mlg-ulb/creditcardfraud"
OUTPUT_DIR = "/opt/airflow/data"


def baixar_dados_kaggle_credit_card_fraud():
    """Baixa e extrai dados do Kaggle"""
    logger.info("Iniciando download do Kaggle...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.system(f"kaggle datasets download -d {KAGGLE_DATASET} -p {OUTPUT_DIR}")

    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(OUTPUT_DIR, file), 'r') as zip_ref:
                zip_ref.extractall(OUTPUT_DIR)
            os.remove(os.path.join(OUTPUT_DIR, file))
    logger.success("Download e extração concluídos.")


def preparar_dados_credit_card():
    """Carrega e trata dataset de cartões de crédito"""
    df = pd.read_csv(f"{OUTPUT_DIR}/creditcard.csv")
    df = df.rename(columns={"Class": "fraude"})
    df['data_part'] = pd.to_datetime('now').strftime('%Y-%m-%d')
    df.to_parquet(f"{OUTPUT_DIR}/creditcard.parquet", index=False)
    logger.success("Dados Kaggle salvos como Parquet.")


if __name__ == "__main__":
    baixar_dados_kaggle_credit_card_fraud()
    preparar_dados_credit_card()