#gerar dados

from faker import Faker
import pandas as pd
import random
import os
from datetime import datetime
from loguru import logger

fake = Faker('pt_BR')

def gerar_dados_bronze(numero=1000):
    tipos = ['PIX', 'TED', 'DOC', 'Cartão']
    bancos = ['001', '237', '104', '341', '033']

    dados = []
    for n in range(numero):
        dados.append({
            "id_transacao": fake.uuid4(),
            "id_cliente": fake.uuid4(),
            "cpf": fake.cpf(),
            "valor": round(random.uniform(-1000, 8000), 2),  # incluir valores inválidos, para simular possiveis erros
            "tipo": random.choice(tipos),
            "banco_origem": random.choice(bancos),
            "banco_destino": random.choice(bancos),
            "data": fake.date_time_between(start_date='-30d', end_date='now').isoformat()
        })

    os.makedirs("/home/leo/airflow/Projeto/bronze", exist_ok=True)
    df = pd.DataFrame(dados)
    df.to_csv("/home/leo/airflow/Projeto/bronze/transacoes_raw.csv", index=False)
    logger.success("Bronze salvo em home/leo/airflow/Projeto/bronze/transacoes_raw.csv")