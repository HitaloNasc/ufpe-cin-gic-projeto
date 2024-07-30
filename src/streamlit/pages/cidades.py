import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pages.campus import *
from templates.navbar import *


def plot_top_10_bairros(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['BAIRRO_ENDERECO'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['BAIRRO_ENDERECO'].isin(top_10)],
                  y='BAIRRO_ENDERECO', order=top_10)
    plt.title('Principais Bairros')
    plt.xlabel('Quantidade')
    plt.ylabel('Bairro')
    plt.tight_layout()
    st.pyplot(plt)


st.set_page_config(layout='wide',
                   page_title="Análise por cidades",
                   page_icon="./images/favicon-ufpe.jpg")

navbar()

st.title("Análise por Cidades")

df = pd.read_json("./datasets/colect-data.json")

cidades = sorted(df['CIDADE_ENDERECO'].unique().tolist())
cidades.append('Todas as cidades')
cidade_selecionada = st.sidebar.multiselect('Selecione as Cidades', cidades, default=['Todas as cidades'])

if 'Todas as cidades' in cidade_selecionada:
    df_filtered = df.copy()
else:
    df_filtered = df[df['CIDADE_ENDERECO'].isin(cidade_selecionada)]

st.header('KPIs')
col1, col2 = st.columns(2)
col1.metric('Total de Ingressantes', len(df_filtered))

sexo_counts = df_filtered['SEXO'].value_counts(normalize=True) * 100
cota_counts = df_filtered['COTA'].value_counts(normalize=True) * 100

charts1, charts2 = st.columns(2)

with charts1:
    st.subheader('Proporção por Sexo')
    plot_sexo_counts(sexo_counts)

    st.subheader('Distribuição por Campus')
    plot_campus(df_filtered)

    st.subheader('Ingressantes por Ano e Semestre')
    plot_ingressantes_por_ano_semestre(df_filtered)


with charts2:
    st.subheader('Proporção por Cotas')
    plot_cota_counts(cota_counts)

    st.subheader('Distribuição por Bairros')
    plot_top_10_bairros(df_filtered)

    st.subheader('Principais cursos')
    plot_top_10_curso(df_filtered)
