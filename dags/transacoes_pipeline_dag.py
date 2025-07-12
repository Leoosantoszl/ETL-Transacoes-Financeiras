from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'leonardo',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='pipeline_transacoes_financeiras',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Pipeline ETL de transações: bronze -> silver -> gold',
    tags=['etl', 'transacoes', 'financeiro'],
) as dag:

    bronze = BashOperator(
        task_id='gerar_dados_bronze',
        bash_command='python /home/leo/airflow/Projeto/src/bronze_ingestor.py'
    )

    silver = BashOperator(
        task_id='limpar_e_padronizar_dados',
        bash_command='python /home/leo/airflow/Projeto/src/silver_cleaner.py'
    )

    gold = BashOperator(
        task_id='enriquecer_dados_gold',
        bash_command='python /home/leo/airflow/Projeto/src/gold_enricher.py'
    )

    contador = BashOperator(
    task_id='contador_de_logs',
    bash_command='python /home/leo/airflow/Projeto/src/utils/contador.py'
    )


    contador >> bronze >> silver >> gold  # dependência sequencial