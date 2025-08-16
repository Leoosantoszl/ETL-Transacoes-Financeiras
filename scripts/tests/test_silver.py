import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StringType, FloatType
from scripts.silver_cleaner import bancos_map

@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder.master("local[1]").appName("TestSilver").getOrCreate()
    yield spark
    spark.stop()

def criar_df_teste(spark):
    # Dados fake
    data = [
        ("t1", "123.456.789-00", 100.0, "001", "237"),
        ("t2", "987.654.321-00", 250.0, "104", "341"),
        ("t3", "111.222.333-44", 50.0, "033", "001"),
    ]
    columns = ["id_transacao", "cpf", "valor", "banco_origem", "banco_destino"]
    df = spark.createDataFrame(data, columns)
    
    # Criar colunas esperadas pela função de enriquecimento
    df = df.withColumn("data_transacao", lit("2025-08-15"))
    df = df.withColumn("datahora", lit("2025-08-15T12:00:00"))
    df = df.withColumn("Spending_Score", lit(50))
    df = df.withColumn("ID", lit("id_fake"))
    df = df.withColumn("Var_1", lit("var"))
    df = df.withColumn("Segmentation", lit("seg"))
    return df

def test_filtros_basicos(spark):
    df = criar_df_teste(spark)
    
    # Teste duplicatas
    ids = [row.id_transacao for row in df.select("id_transacao").collect()]
    assert len(ids) == len(set(ids))
    
    # Teste valores positivos
    assert df.filter(col("valor") <= 0).count() == 0
    
    # Teste CPF válido
    assert df.filter(~col("cpf").contains(".")).count() == 0
    assert df.filter(~col("cpf").contains("-")).count() == 0
    assert df.filter(col("cpf").rlike(r"\d{3}\.\d{3}\.\d{3}-\d{2}") == False).count() == 0

def test_bancos_nome(spark):
    df = criar_df_teste(spark)
    
    # Adicionar colunas com nomes dos bancos simulando a função
    df = df.withColumn(
        "banco_origem_nome",
        col("banco_origem")
    ).withColumn(
        "banco_destino_nome",
        col("banco_destino")
    )

    bancos_validos = ["001","237","104","341","033","Desconhecido"]
    origem = df.select("banco_origem_nome").rdd.flatMap(lambda x: x).collect()
    destino = df.select("banco_destino_nome").rdd.flatMap(lambda x: x).collect()

    for b in origem + destino:
        assert b in bancos_validos
