#criar pasta e arquivo para configurar saida
from loguru import logger
import json
from datetime import datetime
import os

# Caminho absoluto correto para o diretório de logs
log_dir = "/opt/airflow/data/logs"
os.makedirs(log_dir, exist_ok=True)

# Configurar saída de log em formato rotativo
logger.add(f"{log_dir}/exec_{{time}}.log", rotation="1 day", retention="7 days")


def atualizar_contador(path='/opt/airflow/data/logs/contador_transacoes.json', qtd=0):
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

    logger.info(f"Transações atualizadas para {dados[hoje]} no dia {hoje}")
    return dados[hoje]
