import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pages.campus import *


def plot_top_10_bairros(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['BAIRRO_ENDERECO'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['BAIRRO_ENDERECO'].isin(top_10)],
                  y='BAIRRO_ENDERECO', order=top_10)
    plt.title('Principais Bairros')
    plt.xlabel('Quantidade')
    plt.ylabel('Bairro')
    st.pyplot(plt)


st.title("Análise por Cidades")

df = pd.read_json("./datasets/colect-data.json")

cidades = sorted(df['CIDADE_ENDERECO'].unique().tolist())
cidade_selecionada = st.sidebar.selectbox('Selecione a Cidade', cidades)

df_filtered = df.copy()
df_filtered = df_filtered[df_filtered['CIDADE_ENDERECO'] == cidade_selecionada]


st.header('KPIs')
col1, col2 = st.columns(2)
col1.metric('Total de Ingressantes', len(df_filtered))

sexo_counts = df_filtered['SEXO'].value_counts(normalize=True) * 100
cota_counts = df_filtered['COTA'].value_counts(normalize=True) * 100

chart1, chart2 = st.columns(2)

with chart1:
    st.subheader('Proporção por Sexo')
    plot_sexo_counts(sexo_counts)

with chart2:
    st.subheader('Proporção por Cotas')
    plot_cota_counts(cota_counts)

st.header('Distribuição por Campus')
plot_campus(df_filtered)

st.header('Distribuição por Bairros')
plot_top_10_bairros(df_filtered)

st.header('Distribuição de Ingressantes por Ano e Semestre')
plot_ingressantes_por_ano_semestre(df_filtered)

st.header('Principais cursos')
plot_top_10_curso(df_filtered)
