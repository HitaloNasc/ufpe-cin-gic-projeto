import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


def plot_ingressantes_por_ano_semestre(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='ANO_INGRESSO', hue='SEMESTRE_INGRESSO')
    plt.title('Distribuição de Ingressantes por Ano e Semestre')
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Quantidade')
    plt.legend(title='Semestre de Ingresso')
    st.pyplot(plt)


def plot_campus(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='CAMPUS', order=df['CAMPUS'].value_counts().index)
    plt.title('Distribuição por Campus')
    plt.xlabel('Quantidade')
    plt.ylabel('Campus')
    st.pyplot(plt)


def plot_top_10_curso(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['CURSO'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['CURSO'].isin(top_10)], y='CURSO', order=top_10)
    plt.title('Top 10 Cursos')
    plt.xlabel('Quantidade')
    plt.ylabel('Curso')
    st.pyplot(plt)


def plot_top_10_naturalidade(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['NATURALIDADE'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['NATURALIDADE'].isin(top_10)], y='NATURALIDADE', order=top_10)
    plt.title('Top 10 Naturalidades')
    plt.xlabel('Quantidade')
    plt.ylabel('Naturalidade')
    st.pyplot(plt)


def plot_top_10_endereco(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['CIDADE_ENDERECO'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['CIDADE_ENDERECO'].isin(top_10)], y='CIDADE_ENDERECO', order=top_10)
    plt.title('Top 10 Endereços (Cidade)')
    plt.xlabel('Quantidade')
    plt.ylabel('Cidade')
    st.pyplot(plt)


def calcular_matriz_transicao(df):
    transicoes = df.groupby(['CIDADE_ENDERECO', 'CAMPUS']).size().unstack(fill_value=0)

    stochastic_matrix = transicoes.div(transicoes.sum(axis=1), axis=0)

    return stochastic_matrix


df = pd.read_json("./datasets/colect-data.json")

df['IDADE_INGRESSO'] = 2024 - df['ANO_NASC']

st.set_page_config(
    layout="wide",
)

st.title('Dashboard de Análise Social dos Ingressantes na UFPE (2020-2024)')

anos = ['Todos'] + df['ANO_INGRESSO'].unique().tolist()
semestres = ['Todos'] + df['SEMESTRE_INGRESSO'].unique().tolist()
campi = ['Todos'] + df['CAMPUS'].unique().tolist()

ano_selecionado = st.sidebar.selectbox('Selecione o Ano de Ingresso', anos)
semestre_selecionado = st.sidebar.selectbox('Selecione o Semestre de Ingresso', semestres)
campus_selecionado = st.sidebar.selectbox('Selecione o Campus', campi)

df_filtered = df.copy()

if ano_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['ANO_INGRESSO'] == ano_selecionado]
if semestre_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['SEMESTRE_INGRESSO'] == semestre_selecionado]
if campus_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['CAMPUS'] == campus_selecionado]

st.header('KPIs')
col1, col2 = st.columns(2)

col1.metric('Total de Ingressantes', len(df_filtered))
col2.metric('Idade Média dos Ingressantes', f"{round(df_filtered['IDADE_INGRESSO'].mean(), 1)} anos")

sexo_counts = df_filtered['SEXO'].value_counts(normalize=True) * 100
sexo_masc = sexo_counts.get('M', 0)
sexo_fem = sexo_counts.get('F', 0)
col1.write(f"**Proporção por Sexo**")
col1.write(f"Masculino: {sexo_masc:.1f}%")
col1.write(f"Feminino: {sexo_fem:.1f}%")

cota_counts = df_filtered['COTA'].value_counts(normalize=True) * 100
cotas_proporcao = '<br>'.join([f"**{cota}:** {percent:.1f}%" for cota, percent in cota_counts.items()])
col2.write(f"**Proporção por Cotas**", unsafe_allow_html=True)
col2.write(cotas_proporcao, unsafe_allow_html=True)

st.header('Distribuição de Ingressantes por Ano e Semestre')
plot_ingressantes_por_ano_semestre(df_filtered)

st.header('Distribuição por Campus')
plot_campus(df_filtered)

st.header('Top 10 Cursos')
plot_top_10_curso(df_filtered)

st.header('Top 10 Naturalidades')
plot_top_10_naturalidade(df_filtered)

st.header('Top 10 Endereços (Cidade)')
plot_top_10_endereco(df_filtered)

st.header('Matriz Estocástica de Transição: Campus e Cidade de Endereço')
matriz_transicao = calcular_matriz_transicao(df_filtered)
st.write(matriz_transicao)
