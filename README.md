<h1 align="center">💳 Monitoramento de Transações Financeiras com PySpark + Airflow</h1>

<p align="center">
  <strong>Projeto de Engenharia de Dados</strong> com ingestão, processamento e enriquecimento de transações financeiras simuladas.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" />
  <img src="https://img.shields.io/badge/python-3.10-blue" />
  <img src="https://img.shields.io/badge/spark-4.0-orange" />
  <img src="https://img.shields.io/badge/airflow-2.7+-green" />
</p>

---

## 🧭 Visão Geral

Este pipeline ETL simula transações bancárias e as **enriquece com dados públicos** para identificar padrões e facilitar análises. O projeto foca em:

- 🔄 Orquestração com Airflow  
- ⚡ Processamento distribuído com PySpark  
- 🔒 Segurança com mascaramento de dados sensíveis  
- 📈 Escalabilidade e observabilidade  
- 🧱 Arquitetura em camadas (Bronze, Silver, Gold)

---

## ⚙️ Tecnologias Utilizadas

- 🐍 **Python 3.10.12**
- 🔥 **Apache Spark 4.0**
- 🌬️ **Apache Airflow 2.7+**
- 🐘 **PySpark**
- 🐳 **Docker** (opcional, para execução isolada)
- 📦 **Kaggle Datasets + IBGE (dados públicos)**
- 📊 **Streamlit**
---

## 🧱 Arquitetura em Camadas (Medallion Architecture)

| Camada  | Descrição |
|---------|----------|
| 🟤 **Bronze** | Dados simulados brutos gerados com `Faker` |
| ⚪ **Silver** | Dados limpos, validados e enriquecidos |
| 🟡 **Gold**   | Dados mascarados e cruzados com IBGE, Receita e Kaggle |

---

## 📁 Estrutura do Projeto

```bash
.
├── dags/                       # DAGs do Airflow
├── data/                       # Dados particionados por camada (Bronze, Silver, Gold)
├── scripts/                    # Scripts PySpark de transformação
├── dashboard/                  # Scripts Streamlit para visualização de dados
├── docker-compose.yml          # Orquestração com Docker
├── Dockerfile                  # Imagem customizada Airflow + Spark
├── requirements.txt            # Pacotes necessários
└── README.md                   # Este documento



## Dados Utilizados
Simulação de Transações (geradas com Faker)

Kaggle:

creditcard.csv

bank_marketing_full.csv

IBGE: lista de municípios e estados

Receita Federal (simulada): nomes de bancos



### COMO EXECUTAR O PROJETO 
🚀 Como Executar o Projeto
1. Clonar o Repositório

git clone https://github.com/seu-usuario/transacoes-financeiras-pipeline.git
cd transacoes-financeiras-pipeline

2. Criar Ambiente Virtual

python3 -m venv airflow-env
source airflow-env/bin/activate
pip install -r requirements.txt

3. Baixando o kaggle.json
Vá até: https://www.kaggle.com/settings

Role até a seção "API"

Clique em "Create New API Token"

Isso irá baixar o arquivo kaggle.json com seu username e API token

/home/seu_usuario/airflow/Projeto/secrets/kaggle.json ~/.kaggle/

chmod 600 ~/.kaggle/kaggle.json

4. Subir o Airflow e Executar DAG

# Suba o docker 
Utilize o dockerfile para buildar a imagem airflow + Spark

docker-compose build

Depois utilize o comando para subir o docker

docker-compose -d

Acesse: http://localhost:8080
Login padrão: admin | Senha: admin

Ative e execute a DAG: pipeline_transacoes_pyspark



👨‍💻 Autor
Leonardo Oliveira dos Santos
Engenheiro de Dados • Python | PySpark | Airflow 
LinkedIn https://www.linkedin.com/in/leonardo-oliveira-20083b1a2/  • GitHub https://github.com/Leoosantoszl?tab=repositories

