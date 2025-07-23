from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'leonardo',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 15),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='pipeline_transacoes_pyspark',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Pipeline ETL com PySpark: bronze -> silver -> gold',
    tags=['pyspark', 'etl'],
) as dag:

    ingest_bank_marketing = BashOperator(
        task_id='obter_dados_keaggle_bank',
        bash_command='spark-submit /opt/airflow/scripts/ingest_bank_marketing.py'
    )

    ingest_CreditCard_Fraude = BashOperator(
        task_id='obter_dados_keaggle_credit_fraude',
        bash_command='spark-submit /opt/airflow/scripts/ingest_CreditCard_Fraude.py'
    )

    bronze = BashOperator(
        task_id='executar_bronze',
        bash_command='spark-submit /opt/airflow/scripts/bronze_ingestor.py'
    )

    silver = BashOperator(
        task_id='executar_silver',
        bash_command='spark-submit /opt/airflow/scripts/silver_cleaner.py'
    )

    gold = BashOperator(
        task_id='executar_gold',
        bash_command='spark-submit /opt/airflow/scripts/gold_enricher.py'
    )

    contador = BashOperator(
        task_id='executar_contador',
        bash_command='python3 /opt/airflow/scripts/utils/contador.py'
    )

    ingest_CreditCard_Fraude >> ingest_bank_marketing >> contador >> bronze >> silver >> gold 