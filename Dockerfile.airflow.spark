FROM apache/airflow:2.8.1-python3.10

USER root

# Instala ferramentas essenciais
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl unzip ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y procps

# Instala OpenJDK 11
RUN mkdir -p /opt/java && \
    curl -L -o /tmp/jdk.tar.gz https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21+9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.21_9.tar.gz && \
    tar -xzf /tmp/jdk.tar.gz -C /opt/java --strip-components=1 && \
    rm /tmp/jdk.tar.gz

ENV JAVA_HOME=/opt/java
ENV PATH="$JAVA_HOME/bin:$PATH"

# Instala Apache Spark
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3

RUN curl -L -o /tmp/spark.tgz https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf /tmp/spark.tgz -C /opt && \
    ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm /tmp/spark.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH="$PATH:$SPARK_HOME/bin"

# Troca para o usuário airflow para instalar pacotes Python
USER airflow

# Instala bibliotecas Python do projeto como usuário airflow
RUN pip install \
    pyspark==3.5.0 \
    pandas \
    pyarrow \
    requests \
    loguru \
    kaggle \
    faker

# Executa como root
USER root

# Cria o diretório e copia o kaggle.json
RUN mkdir -p /home/airflow/.kaggle
COPY secrets/kaggle.json /home/airflow/.kaggle/kaggle.json

# Define permissões corretas
RUN chmod 600 /home/airflow/.kaggle/kaggle.json && \
    chown -R airflow: /home/airflow/.kaggle && \
    chmod +x /home/airflow/.local/bin/kaggle

# Volta para o usuário padrão
USER airflow



