import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pyarrow import dataset as ds

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Transações Financeiras")

@st.cache_data
def carregar_dados():
    path = "/opt/airflow/data/Gold"

    if not os.path.exists(path):
        st.warning(f"⚠️ Caminho não encontrado: {path}")
        return pd.DataFrame()
    try:
        # Usa pyarrow.dataset para ler todas as partições
        dataset = ds.dataset(path, format="parquet", partitioning="hive")
        df = dataset.to_table().to_pandas()
        st.success("✅ Dados carregados com sucesso!")
        return df
    except Exception as e:
        st.error(f"⚠️ Erro ao carregar dados particionados: {e}")
        return pd.DataFrame()

# 🟡 Aqui você chama a função e armazena o resultado
df = carregar_dados()

# 🚨 Se o DataFrame estiver vazio, avisa e para aqui
if df.empty:
    st.warning("Nenhum dado carregado. Verifique o caminho e os arquivos.")
    st.stop()

# Exibir colunas
# st.write("Colunas disponíveis no DataFrame:")
# st.write(df.columns.tolist())

# Conversão de data se necessário
if "data_transacao" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["data_transacao"]):
    df["data_transacao"] = pd.to_datetime(df["data_transacao"])

# Métricas principais
st.metric("📌 Total de Transações", df.shape[0])
st.metric("🚨 Total de Fraudes", int(df["fraude"].sum()))
st.metric("📉 % Fraudes", f'{100 * df["fraude"].mean():.2f}%')

# Gráfico: Transações por Dia
fig1 = px.histogram(df, x="data_transacao", color="fraude", barmode="group",
                    title="📅 Transações por Dia (com Fraudes)")
st.plotly_chart(fig1, use_container_width=True)

# Gráfico: Valor por Banco de Origem
fig2 = px.box(df, x="banco_origem_nome", y="valor", color="fraude",
              title="🏦 Distribuição de Valores por Banco de Origem")
st.plotly_chart(fig2, use_container_width=True)

# Gráfico: Fraudes por Estado
st.subheader("📍 Fraudes por Estado (Mapa de Calor)")
fraudes_estado = df[df["fraude"] == 1]["estado"].value_counts().reset_index()
fraudes_estado.columns = ["estado", "qtd_fraudes"]

fig3 = px.choropleth(
    fraudes_estado,
    locations="estado",
    locationmode="country names",
    color="qtd_fraudes",
    scope="south america",
    color_continuous_scale="Reds",
    title="Mapa de Calor de Fraudes por Estado"
)
st.plotly_chart(fig3, use_container_width=True)

# Gráfico: Fraudes por Banco
st.subheader("🏦 Fraudes por Banco de Origem")
fraudes_banco = df[df["fraude"] == 1]["banco_origem_nome"].value_counts().nlargest(10).reset_index()
fraudes_banco.columns = ["Banco", "Fraudes"]

fig4 = px.bar(fraudes_banco, x="Banco", y="Fraudes", color="Fraudes", title="Top 10 Bancos com Mais Fraudes")
st.plotly_chart(fig4, use_container_width=True)

#  Distribuição de Transações por Hora do Dia
st.subheader("🕒 Distribuição de Transações por Hora do Dia")

# Garantir que 'hora_transacao' está no formato hora
if "hora_transacao" in df.columns:
    try:
        df["hora"] = pd.to_datetime(df["hora_transacao"], format="%H:%M").dt.hour
    except:
        df["hora"] = pd.to_datetime(df["hora_transacao"]).dt.hour

    transacoes_por_hora = df.groupby("hora").size().reset_index(name="qtd_transacoes")
    fig_hora = px.bar(transacoes_por_hora, x="hora", y="qtd_transacoes", title="⏰ Transações por Hora do Dia")
    st.plotly_chart(fig_hora, use_container_width=True)

# Valor Médio das Transações por Estado
st.subheader("🌎 Valor Médio das Transações por Estado")

if "estado" in df.columns and "valor" in df.columns:
    media_estado = df.groupby("estado")["valor"].mean().reset_index()
    fig_valor_estado = px.bar(media_estado, x="estado", y="valor", title="💰 Valor Médio das Transações por Estado")
    st.plotly_chart(fig_valor_estado, use_container_width=True)

# Mapa (se houver latitude e longitude)
if {"latitude", "longitude"}.issubset(df.columns):
    st.subheader("🗺️ Localização das Transações (Se disponível)")
    st.map(df[["latitude", "longitude"]])

# Footer
st.caption("Desenvolvido por Leonardo Santos • Projeto de Engenharia de Dados 💼")
