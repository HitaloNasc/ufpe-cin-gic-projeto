import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
from templates.navbar import *

st.set_page_config(layout='wide',
                   page_title="Ingressantes SISU UFPE",
                   page_icon="./images/favicon-ufpe.jpg")

navbar()

df = pd.read_json("./datasets/colect-data.json")

campi = df["CAMPUS"].unique().tolist()
campus_selecionado = st.sidebar.selectbox("Selecione o Campus", campi)

df_filtered = df.copy()
df_filtered = df_filtered[(df_filtered['CAMPUS'] == campus_selecionado)]

if campus_selecionado != "Todos":
    df_filtered = df_filtered[df_filtered["CAMPUS"] == campus_selecionado]


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
    title="Distribuição de alunos por cidades"
)

fig.update_geos(
    fitbounds="locations",
    visible=False,
)

st.plotly_chart(fig)
