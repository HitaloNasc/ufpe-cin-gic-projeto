import pandas as pd
import plotly.express as px
from pages.campus import *
from templates.navbar import *
import streamlit as st

st.set_page_config(layout='wide',
                   page_title="Ingressantes SISU UFPE",
                   page_icon="./images/favicon-ufpe.jpg")

colors = px.colors.qualitative.Plotly


def plot_top_10_bairros(df):
    top_10 = df["BAIRRO_ENDERECO"].value_counts().nlargest(10).index
    bairros_df = df[df["BAIRRO_ENDERECO"].isin(top_10)]

    fig = px.bar(
        bairros_df,
        y="BAIRRO_ENDERECO",
        color="BAIRRO_ENDERECO",
        category_orders={"BAIRRO_ENDERECO": top_10},
        title="Principais Bairros",
        labels={"BAIRRO_ENDERECO": "Bairro", "count": "Quantidade"},
        color_discrete_sequence=colors,
    )
    fig.update_layout(width=800, height=500)
    st.plotly_chart(fig, use_container_width=True)


navbar()

st.title("Análise por Cidades")

df = pd.read_json("./datasets/colect-data.json")

cidades = sorted(df["CIDADE_ENDERECO"].unique().tolist())
cidades.append("Todas as cidades")
cidade_selecionada = st.sidebar.multiselect(
    "Selecione as Cidades", cidades, default=["Todas as cidades"]
)

if "Todas as cidades" in cidade_selecionada:
    df_filtered = df.copy()
else:
    df_filtered = df[df["CIDADE_ENDERECO"].isin(cidade_selecionada)]

st.header("KPIs")
col1, col2 = st.columns(2)
col1.metric("Total de Ingressantes", len(df_filtered))

sexo_counts = df_filtered["SEXO"].value_counts(normalize=True) * 100
cota_counts = df_filtered["COTA"].value_counts(normalize=True) * 100

charts1, charts2 = st.columns(2)

with charts1:
    st.subheader("Proporção por Sexo")
    plot_sexo_counts(sexo_counts)

    st.subheader("Distribuição por Campus")
    plot_campus(df_filtered)

    st.subheader("Ingressantes por Ano e Semestre")
    plot_ingressantes_por_ano_semestre(df_filtered)

with charts2:
    st.subheader("Proporção por Cotas")
    plot_cota_counts(cota_counts)

    st.subheader("Distribuição por Bairros")
    plot_top_10_bairros(df_filtered)

    st.subheader("Principais cursos")
    plot_top_10_curso(df_filtered)
