import os
import zipfile
import pandas as pd
from loguru import logger

KAGGLE_DATASET = "janiobachmann/bank-marketing-dataset"
OUTPUT_DIR = "/opt/airflow/data/kaggle_data/bank_marketing"

def baixar_dados_bank_marketing():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger.info("Baixando Bank Marketing dataset...")
    os.system(f"kaggle datasets download -d {KAGGLE_DATASET} -p {OUTPUT_DIR}")
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(OUTPUT_DIR, f), 'r') as z:
                z.extractall(OUTPUT_DIR)
            os.remove(os.path.join(OUTPUT_DIR, f))
    logger.success("Download e extração concluídos.")

def converter_parquet():
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "bank.csv"))
    df['data_part'] = pd.to_datetime('now').strftime('%Y-%m-%d')
    df.to_parquet(f"{OUTPUT_DIR}/bank_marketing.parquet",index=False)
    logger.success("Bank Marketing salvo como Parquet.")

if __name__ == "__main__":
    baixar_dados_bank_marketing()
    converter_parquet()