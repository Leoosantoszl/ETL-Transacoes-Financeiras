import pandas as pd
import os
from datetime import datetime
from loguru import logger

def validar_cpf(cpf):
    return isinstance(cpf, str) and len(cpf) == 14 and cpf.count('.') == 2 and '-' in cpf

def limpar_dados_silver():
    df = pd.read_csv("home/leo/airflow/Projeto/bronze/transacoes_raw.csv")

    df = df.drop_duplicates()
    df = df[df['valor'] > 0]
    df = df[df['cpf'].apply(validar_cpf)]
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df = df[df['data'].notnull()]

    os.makedirs("home/leo/airflow/Projeto/silver", exist_ok=True)
    df.to_csv("home/leo/airflow/Projeto/silver/transacoes_limpo.csv", index=False)
    logger.success("Dados Silver salvo em home/leo/airflow/Projeto/silver/transacoes_limpo.csv")
