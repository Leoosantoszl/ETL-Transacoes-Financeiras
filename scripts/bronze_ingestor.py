#gerar dados
from faker import Faker
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, rand, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType,FloatType, TimestampType
import random
import os
from datetime import datetime, timedelta

fake = Faker('pt_BR')
spark = SparkSession.builder.appName("GerarDadosBronze").getOrCreate()

tipos = ['PIX', 'TED', 'DOC', 'Cartão']
bancos = ['001', '237', '104', '341', '033']
generos = ['Masculino', 'Feminino','Outro']
escolaridades = ["Ensino Médio", "Técnico","Superior Incompleto", "Superior Completo",
                 "Pós-graduação", "Mestrado", "Doutorado"]

# Geração de dados fake com hora e histórico
historico_clientes = {}
dados = []
numero = 20000

for _ in range(numero):
    cliente_id = fake.uuid4()
    if cliente_id not in historico_clientes:
        historico_clientes[cliente_id] = {
            "score_credito": random.randint(300, 850)
        }

    valor = round(random.uniform(-1000, 8000), 2)
    data_hora = fake.date_time_between(start_date='-30d', end_date='now')

    dados.append({
        "id_transacao": fake.uuid4(),
        "id_cliente": cliente_id,
        "cpf": fake.cpf(),
        "genero": random.choice(generos),
        "idade" :random.randint(18, 90),
        "profissao" :fake.job(),
        "escolaridade": random.choice(escolaridades),
        "valor": valor,
        "tipo": random.choice(tipos),
        "banco_origem": random.choice(bancos),
        "banco_destino": random.choice(bancos),
        "data_transacao": data_hora.strftime('%Y-%m-%d'),
        "hora_transacao": data_hora.strftime('%H:%M:%S'),
        "datahora": data_hora.isoformat(),
        "score_credito": historico_clientes[cliente_id]["score_credito"],
        "clima": random.choice(["Ensolarado", "Chuva", "Nublado", "Tempestade", "Neve"])
    })

schema = StructType([
    StructField("id_transacao", StringType(), True),
    StructField("id_cliente", StringType(), True),
    StructField("cpf", StringType(), True),
    StructField("genero",StringType(),True),
    StructField("idade",IntegerType(),True),
    StructField("valor", FloatType(), True),
    StructField("tipo", StringType(), True),
    StructField("banco_origem", StringType(), True),
    StructField("banco_destino", StringType(), True),
    StructField("data_transacao", StringType(), True),
    StructField("hora_transacao", StringType(), True),
    StructField("datahora", StringType(), True),
    StructField("score_credito", StringType(), True),
    StructField("clima", StringType(), True),
    StructField("escolaridade", StringType(), True),
    StructField("profissao", StringType(), True)
])

df = spark.createDataFrame(dados, schema)
df = df.withColumn("timestamp_carga", current_timestamp())

# Salvar como Parquet particionado por data
output_path = "/opt/airflow/data/Bronze"
df.write.mode("overwrite").partitionBy("data_transacao").parquet(output_path)

print(f"Dados bronze salvos em {output_path}")
