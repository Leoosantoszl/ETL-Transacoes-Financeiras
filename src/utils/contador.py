#criar pasta e arquivo para configurar saida
from loguru import logger
import json
from datetime import datetime
import os

# Criar diretório de logs
os.makedirs("home/leo/airflow/Projeto/logs", exist_ok=True)

# Configurar saída de log
logger.add("home/leo/airflow/Projeto/logs/exec_{time}.log", rotation="1 day", retention="7 days")


def atualizar_contador(path='home/leo/airflow/Projeto/logs/contador_transacoes.json', qtd=0):
    hoje = datetime.now().strftime('%Y-%m-%d')

    if os.path.exists(path):
        with open(path, 'r') as f:
            dados = json.load(f)
    else:
        dados = {}

    # Atualiza o contador do dia
    dados[hoje] = dados.get(hoje, 0) + qtd

    with open(path, 'w') as f:
        json.dump(dados, f, indent=2)

    return dados[hoje]