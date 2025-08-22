<h1 align="center">💳 Monitoramento de Transações Financeiras com PySpark + Airflow</h1>

<p align="center">
  <strong>Projeto de Engenharia de Dados</strong> com ingestão, processamento e enriquecimento de transações financeiras simuladas.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-concluído-brightgreen" />
  <img src="https://img.shields.io/badge/python-3.10-blue" />
  <img src="https://img.shields.io/badge/spark-4.0-orange" />
  <img src="https://img.shields.io/badge/airflow-2.7+-green" />
  <img src="https://img.shields.io/badge/terraform-Azure-blueviolet" />
</p>

---

## 🧭 Visão Geral

Este pipeline ETL simula transações bancárias e as **enriquece com dados públicos** para identificar padrões e facilitar análises e realizar um modelo de machine learning que nos ajuda a prever fraudes.

Principais recursos:

- 🔄 Orquestração com **Apache Airflow**  
- ⚡ Processamento distribuído com **PySpark**  
- 🔒 Segurança com mascaramento de dados sensíveis  
- 📈 Escalabilidade e observabilidade  
- 🧱 Arquitetura em camadas (**Bronze, Silver, Gold**)

---

## ⚙️ Tecnologias Utilizadas

- 🐍 **Python 3.10.12**
- 🔥 **Apache Spark 4.0**
- 🌬️ **Apache Airflow 2.7+**
- 🐘 **PySpark**
- 🐳 **Docker + Docker Compose**
- 📦 **Kaggle Datasets + IBGE (dados públicos)**
- 📊 **Streamlit**
- 🐘 **PostgreSQL**
- ☁️ **Azure Virtual Machine**
- 📜 **Terraform** (Infra como Código)

---

## 🧱 Arquitetura em Camadas (Medallion Architecture)

| Camada  | Descrição |
|---------|----------|
| 🟤 **Bronze** | Dados brutos simulados com `Faker` |
| ⚪ **Silver** | Dados limpos, validados e enriquecidos |
| 🟡 **Gold**   | Dados mascarados e integrados com dados públicos |

---

## 📁 Estrutura do Projeto

```bash
.
├── dags/                       # DAGs do Airflow
├── data/                       # Dados particionados (Bronze, Silver, Gold)
├── tests/
│   ├── test_silver.py           # Testes de funções da camada Silver
│   └── test_gold.py             # Testes de funções da camada Gold
│
├── scripts/                    # Scripts PySpark
├── docker-compose.yml          # Orquestração de containers
├── Dockerfile.airflow.spark    # Airflow + Spark
├── Dockerfile.streamlit        # Dashboard Streamlit
├── requirements.txt            # Dependências
├── secrets/                    # Contém kaggle.json (não versionado)
├── infra/
│   └── terraform/              # Código IaC para Azure
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── outputs.tf
└── README.md



📊 Dados Utilizados

Simulação: Geradas com Faker

Kaggle:

creditcard.csv

bank_marketing_full.csv

IBGE: Municípios e Estados

Receita Federal (simulada): Nomes de bancos

Lembrando que podemos executar de forma local ou cloud (Azure)


☁️ Deploy na Azure com Terraform
1️⃣ Instalar Dependências

Azure 

Instale a Azure CLI (caso ainda não tenha):
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

Faça login na Azure
az login --use-device-code
az login
az account show


Se você tiver múltiplas assinaturas:
az account set --subscription "ID-ou-Nome-da-Sua-Subscription"


# Terraform
Passo a passo para instalar o Terraform (Linux/WSL)
Instalar dependências:

sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl unzip
Adicionar o repositório oficial do Terraform:

curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/hashicorp.gpg
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
Instalar o Terraform:

sudo apt-get update && sudo apt-get install terraform
Verificar instalação:

terraform -v

2️⃣ Autenticar na Azure
az login --use-device-code
az account set --subscription "SUA_SUBSCRIPTION"

3️⃣ Pegar arquivos do Git

git clone https://github.com/Leoosantoszl/ETL-Transacoes-Financeiras.git
cd projeto

4️⃣ Configurar kaggle.json
Fora da VM:
Vá até: https://www.kaggle.com/settings
faça login com sua conta

Na seção API, clique em Create New API Token

Isso irá baixar kaggle.json

Agora podemos seguir com o projeto:

5️⃣ Provisionar Infraestrutura

cd projeto/IAC/terraform
terraform init
terraform plan
terraform apply

Isso criará a VM com Docker, Docker Compose e o projeto já configurado via cloud-init.

6️⃣ - Conectar na VM, instalar dependencias, e rodar projeto
ssh azureuser@IP_DA_VM

Instale as dependencias

cd projeto

pip install -r requirements.txt

Após instalar as dependencias na sua VM, vá na sua maquina onde foi baixado o arquivo kaggle.json
Rode o comando para transferir o arquivo para sua VM, lembrando de alterar o caminho do arquivo e o IP da VM
normalmente por padrão a chave rsa fica nesse diretorio(só confira se a sua está)

scp -i ~/.ssh/id_rsa (caminho arquivo)/kaggle.json azureuser@(IP VM):/home/azureuser/

E coloque sua senha rsa
Agora dentro da VM:
Mova o arquivo para o diretorio secrets dentro do projeto e de permissão para ele:

mv ~/kaggle.json projeto/secrets/
chmod 600 ~/projeto/secrets/kaggle.json

Depois acesse a pasta do projeto e rode o comando

sudo docker-compose up -d

A aplicação já estará rodando e o Airflow acessível pelo IP público na porta 8080

apos o processamento da camada Gold, entre no streamlit para ver os resultados.
acesse: IP_VM:8051
os graficos com os insights do projeto estaram disponivel la.

Agora de forma local:

🚀 Como Executar Localmente
1️⃣ Clonar o Repositório
git clone https://github.com/Leoosantoszl/ETL-Transacoes-Financeiras.git
cd projeto

2️⃣ Criar e Ativar Ambiente Virtual

python3 -m venv airflow-env
source airflow-env/bin/activate
pip install -r requirements.txt

3️⃣ Configurar kaggle.json

Vá até: https://www.kaggle.com/settings

Na seção API, clique em Create New API Token

Isso irá baixar kaggle.json

Mova o arquivo para:

mkdir -p secrets
mv ~/Downloads/kaggle.json secrets/
chmod 600 secrets/kaggle.json

4️⃣ Subir Containers
docker compose build (Caso não tenha as imagens que veem no projeto)
docker compose up -d


Acesse Airflow: http://localhost:8080
Usuário: admin
Senha: admin

Ative e execute a DAG pipeline_transacoes_pyspark

🧪 Testes

O projeto possui testes automatizados para as camadas Silver e Gold, garantindo que a transformação e o enriquecimento dos dados estejam corretos.

1. Pré-requisitos

Ter o Python 3.10+ instalado.

Ter o PySpark instalado (pip install pyspark).

Ter o pytest instalado (pip install pytest).

2. Estrutura dos testes

scripts/tests/test_silver.py: Testa funções de limpeza e enriquecimento da camada Silver, incluindo filtros de CPF, valores e nomes de bancos.

scripts/tests/test_gold.py: Testa funções da camada Gold, como mascaramento de CPF e reorganização de colunas.

rode o comando
PYTHONPATH=$(pwd) pytest



👨‍💻 Autor
Leonardo Oliveira dos Santos
Engenheiro de Dados | Python | PySpark | Airflow | Docker | Terraform |
LinkedIn https://www.linkedin.com/in/leonardo-oliveira-20083b1a2/  • GitHub https://github.com/Leoosantoszl?tab=repositories


