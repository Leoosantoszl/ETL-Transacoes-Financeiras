import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, to_date, date_format
from pyspark.sql.types import StringType
from loguru import logger


# Função para mascarar CPF
def mascarar_cpf(cpf: str) -> str:
    if cpf is None:
        return "None.***.***-**"
    if len(cpf) >= 11:
        return cpf[:3] + ".***.***-" + cpf[-2:]
    return cpf[:3] + ".***.***-**"

mascarar_udf = udf(mascarar_cpf, StringType())

def transformar_para_gold():
    spark = SparkSession.builder.appName("GoldLayer").getOrCreate()

    logger.info("📥 Lendo dados da camada Silver...")
    df = spark.read.parquet("/opt/airflow/data/Silver")

    # Aplicar mascaramento de CPF
    df = df.withColumn("cpf", mascarar_udf(col("cpf")))

    # Garantir data_part para particionamento
    df = df.withColumn("data_part", to_date("data_transacao"))
    #tratamento data transacao
    df = df.withColumn("data_transacao", date_format("data_transacao", "dd/MM/yyyy"))
    # Reorganizar colunas principais
    colunas_desejadas = [
        "id_transacao", "id_cliente", "cpf", "genero", "idade",
        "banco_origem_nome", "banco_destino_nome", "valor", "data_transacao",
        "cidade", "estado", "profissao", "escolaridade", "emprestimo","fraude"
    ]

    colunas_existentes = [c for c in colunas_desejadas if c in df.columns]
    colunas_ordenadas = colunas_existentes + [c for c in df.columns if c not in colunas_existentes]
    df = df.select(colunas_ordenadas)

    logger.info(f"💾 Salvando camada Gold particionada por 'data_part'...")
    df.write.mode("overwrite").partitionBy("data_part").parquet("/opt/airflow/data/Gold")

    logger.success("✅ Camada Gold gerada com sucesso.")
    spark.stop()

if __name__ == "__main__":
    transformar_para_gold()

