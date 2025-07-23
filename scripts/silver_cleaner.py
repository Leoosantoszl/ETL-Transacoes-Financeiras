from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, length, row_number, lit, udf, when
from pyspark.sql.types import StringType
from pyspark.sql.window import Window
from loguru import logger
import requests
import random

def buscar_municipios_do_ibge():
    try:
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            municipios = resp.json()
            lista = []
            for m in municipios:
                try:
                    nome = m['nome']
                    uf = m['microrregiao']['mesorregiao']['UF']['sigla']
                    lista.append((nome, uf))
                except Exception:
                    lista.append(("Desconhecido", "??"))
            return lista
        else:
            logger.error(f"Erro ao acessar IBGE: {resp.status_code}")
    except Exception as e:
        logger.error(f"Erro inesperado IBGE: {e}")
    return [("Desconhecido", "??")]

bancos_map = {
    "001": "Banco do Brasil",
    "237": "Bradesco",
    "104": "Caixa Econômica Federal",
    "341": "Itaú Unibanco",
    "033": "Santander"
}


def limpar_e_enriquecer_dados_silver():
    spark = SparkSession.builder \
        .appName("SilverEnrichment") \
        .config("spark.sql.shuffle.partitions", "4") \
        .getOrCreate()

    df = spark.read.parquet("/opt/airflow/data/Bronze")

    df = df.dropDuplicates(["id_transacao"]) \
           .filter(col("valor") > 0) \
           .filter(length("cpf") == 14) \
           .filter(col("cpf").contains(".")) \
           .filter(col("cpf").contains("-")) \
           .withColumn("data_transacao", to_timestamp("data_transacao"))
       
    # Normalizar banco para string 3 dígitos com zero à esquerda
    df = df.withColumn("banco_origem", col("banco_origem").cast("string"))
    df = df.withColumn("banco_destino", col("banco_destino").cast("string"))

    # Condições bancos com when      
    df = df.withColumn(
        "banco_origem_nome",
        when(col("banco_origem") == "001", bancos_map["001"])
        .when(col("banco_origem") == "237", bancos_map["237"])
        .when(col("banco_origem") == "104", bancos_map["104"])
        .when(col("banco_origem") == "341", bancos_map["341"])
        .when(col("banco_origem") == "033", bancos_map["033"])
        .otherwise("Desconhecido")
    )

    df = df.withColumn(
        "banco_destino_nome",
        when(col("banco_destino") == "001", bancos_map["001"])
        .when(col("banco_destino") == "237", bancos_map["237"])
        .when(col("banco_destino") == "104", bancos_map["104"])
        .when(col("banco_destino") == "341", bancos_map["341"])
        .when(col("banco_destino") == "033", bancos_map["033"])
        .otherwise("Desconhecido")
    )

    logger.info(f"📊 Bronze tratada: {df.count()} registros válidos.")

    municipios = buscar_municipios_do_ibge()
    cidades = [m[0] for m in municipios]
    estados = [m[1] for m in municipios]

    cidades_broadcast = spark.sparkContext.broadcast(cidades)
    estados_broadcast = spark.sparkContext.broadcast(estados)

    def cidade_aleatoria(_): return random.choice(cidades_broadcast.value)
    def estado_aleatoria(_): return random.choice(estados_broadcast.value)

    cidade_udf = udf(cidade_aleatoria, StringType())
    estado_udf = udf(estado_aleatoria, StringType())

    df = df.withColumn("cidade", cidade_udf(lit(1)))
    df = df.withColumn("estado", estado_udf(lit(1)))


    # Criação de row_num para junções randômicas
    df = df.withColumn("row_num", row_number().over(Window.orderBy("id_transacao")))

    try:
        df_fraude = spark.read.parquet("/opt/airflow/data/kaggle_data/creditcardfraud/creditcard.parquet") \
                              .withColumnRenamed("Class", "fraude")
        logger.success("✅ creditcard.parquet carregado com sucesso.")
        # Se necessário usar no futuro, merge pode ser feito via row_num
    except Exception as e:
        logger.warning(f"⚠️ Erro ao carregar creditcard.parquet: {e}")
        df_fraude = None

    try:
        df_marketing = spark.read.parquet("/opt/airflow/data/kaggle_data/bank_marketing/bank_marketing.parquet") \
                                 .select(
                                     col("job").alias("ocupacao"),
                                     col("loan").alias("emprestimo"))
        df_marketing = df_marketing.withColumn("row_num", row_number().over(Window.orderBy("ocupacao")))
        df = df.join(df_marketing, on="row_num", how="left")
        logger.success("✅ bank.parquet enriquecido com sucesso.")
    except Exception as e:
        logger.warning(f"⚠️ Erro ao carregar bank_marketing.parquet: {e}")

    #drop cols 
    df = df.drop("row_num","Spending_Score","datahora","ocupacao","ID","Var_1","Segmentation","banco_origem","banco_destino")

    df.write.mode("overwrite").parquet("/opt/airflow/data/Silver")
    logger.success("✅ Dados enriquecidos salvos na camada Silver com sucesso")

if __name__ == "__main__":
    limpar_e_enriquecer_dados_silver()

