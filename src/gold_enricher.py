import pandas as pd
import requests
import os
import random
from loguru import logger

bancos = {
    "001": "Banco do Brasil",
    "237": "Bradesco",
    "104": "Caixa Econômica Federal",
    "341": "Itaú Unibanco",
    "033": "Santander"
}

def mascarar_cpf(cpf):
    return f"***.{cpf[4:7]}.***-{cpf[-2:]}"


def buscar_municipios_do_ibge():
    """
    Retorna uma lista de tuplas com nome da cidade e sigla do estado (UF).
    Exemplo: (["São Paulo", "Campinas"], ["SP", "SP"])
    """
    try:
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            municipios = resp.json()
            nome = []
            uf = []

            for v in municipios:
                try:
                    nome.append(v['nome'])
                    uf.append(v['microrregiao']['mesorregiao']['UF']['sigla'])
                except (TypeError, KeyError):
                    nome.append("Desconhecido")
                    uf.append("Desconhecido")

            return nome, uf

        else:
            logger.error(f"Erro ao acessar API do IBGE. Código: {resp.status_code}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")

    # Fallback padrão
    return ["Desconhecido"], ["Desconhecido"]



def enriquecer_dados_gold():
    df = pd.read_csv("home/leo/airflow/Projeto/silver/transacoes_limpo.csv")
    municipios = buscar_municipios_do_ibge()

    # Enriquecimento com bancos e localização
    df['banco_origem'] = df['banco_origem'].astype(str).str.strip().str.zfill(3) #normalizar dados,
    df['banco_destino'] = df['banco_destino'].astype(str).str.strip().str.zfill(3)
    df['banco_origem_nome'] = df['banco_origem'].map(bancos)
    df['banco_destino_nome'] = df['banco_destino'].map(bancos)
    df['cpf_mascarado'] = df['cpf'].apply(mascarar_cpf)

    if municipios:
        nomes, ufs = municipios  # já são listas separadas
        df['cidade'] = random.choices(nomes, k=len(df))
        df['estado'] = random.choices(ufs, k=len(df))
    else:
        df['cidade'] = "Desconhecida"
        df['estado'] = "??"

    df = df.drop(columns=['cpf'])

    os.makedirs("home/leo/airflow/Projeto/gold", exist_ok=True)
    df.to_csv("home/leo/airflow/Projeto/gold/transacoes_enriquecidas.csv", index=False)
    logger.success(" Gold salvo em home/leo/airflow/Projeto/gold/transacoes_enriquecidas.csv")


    qtd = len(df)
    total = atualizar_contador(qtd=qtd)
    logger.info(f"{qtd} transações processadas nesta execução. Total acumulado do dia: {total}")