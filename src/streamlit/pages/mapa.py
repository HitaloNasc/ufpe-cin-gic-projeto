import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
from templates.navbar import *

def calcular_matriz_transicao(df):
    transicoes = df.groupby(["CIDADE_ENDERECO", "CAMPUS"]
                            ).size().unstack(fill_value=0)
    stochastic_matrix = transicoes.div(transicoes.sum(axis=1), axis=0)
    return stochastic_matrix

st.set_page_config(layout='wide',
                   page_title="Ingressantes SISU UFPE",
                   page_icon="./images/favicon-ufpe.jpg")

navbar()

df = pd.read_json("./datasets/colect-data.json")

campi = ['Todos'] + df["CAMPUS"].unique().tolist()
campus_selecionado = st.sidebar.selectbox("Selecione o Campus", campi)

anos = ['Todos'] + df["ANO_INGRESSO"].unique().tolist()
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos)

df_filtered = df.copy()

if campus_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['CAMPUS'] == campus_selecionado]

if ano_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['ANO_INGRESSO'] == ano_selecionado]


cidades_contagem = df_filtered['CIDADE_ENDERECO'].value_counts().reset_index()
cidades_contagem.columns = ['municipio', 'quantidade']

with open('./datasets/mapa-pernambuco.geojson') as f:
    geojson = json.load(f)


geo_df = pd.DataFrame([
    {'municipio': feature['properties']['NM_MUN']}
    for feature in geojson['features']
])

map_data = geo_df.merge(cidades_contagem, on='municipio', how='left')
map_data['quantidade'].fillna(0, inplace=True)

# Escala logarítmica para normalizar os dados
map_data['log_quantidade'] = np.log1p(map_data['quantidade'])

fig = px.choropleth(
    map_data,
    geojson=geojson,
    locations='municipio',
    featureidkey="properties.NM_MUN",
    color='log_quantidade',
    color_continuous_scale="OrRd",
    range_color=[0, map_data['log_quantidade'].max()],
    title="Distribuição de alunos por cidades",
    labels={'log_quantidade': 'Escala logarítmica'},
    hover_data={
        'municipio': True,
        'quantidade': True
    }
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

st.plotly_chart(fig, use_container_width=True)

df_matriz = df.copy()

if ano_selecionado != 'Todos':
    df_matriz = df_matriz[df_matriz['ANO_INGRESSO'] == ano_selecionado]

st.subheader("Matriz de Transição")
matriz_transicao = calcular_matriz_transicao(df_matriz)
st.write(matriz_transicao)
