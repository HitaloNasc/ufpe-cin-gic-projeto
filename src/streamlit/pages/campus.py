import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def plot_sexo_counts(sexo_counts):
    sexo_counts = sexo_counts.rename(index={'M': 'Masculino', 'F': 'Feminino'})
    sexo_df = pd.DataFrame(
        {'Sexo': sexo_counts.index, 'Proporção': sexo_counts.values})
    fig = px.pie(sexo_df, values='Proporção',
                 names='Sexo', template='plotly_dark')
    fig.update_traces(textposition='inside',
                      textinfo='percent+label', insidetextfont=dict(size=20))
    fig.update_layout(width=350, height=350)
    plt.tight_layout()
    st.plotly_chart(fig, use_container_width=True)


def plot_cota_counts(cota_counts):
    cota_counts = cota_counts.rename(index={'S': 'Sim', 'N': 'Não'})
    cota_df = pd.DataFrame(
        {'Cota': cota_counts.index, 'Proporção': cota_counts.values})
    fig = px.pie(cota_df, values='Proporção', names='Cota', template='gridon')
    fig.update_traces(textposition='inside',
                      textinfo='percent+label', insidetextfont=dict(size=20))
    fig.update_layout(width=350, height=350)
    plt.tight_layout()
    st.plotly_chart(fig, use_container_width=True)


def plot_ingressantes_por_ano_semestre(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='ANO_INGRESSO', hue='SEMESTRE_INGRESSO')
    plt.title('Distribuição de Ingressantes por Ano e Semestre')
    plt.xlabel('Ano de Ingresso')
    plt.ylabel('Quantidade')
    plt.legend(title='Semestre de Ingresso')
    plt.tight_layout()
    st.pyplot(plt)


def plot_campus(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='CAMPUS', order=df['CAMPUS'].value_counts().index)
    plt.title('Distribuição por Campus')
    plt.xlabel('Quantidade')
    plt.ylabel('Campus')
    plt.tight_layout()
    st.pyplot(plt)


def plot_top_10_curso(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['CURSO'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['CURSO'].isin(top_10)], y='CURSO', order=top_10)
    plt.title('Top 10 Cursos')
    plt.xlabel('Quantidade')
    plt.ylabel('Curso')
    plt.tight_layout()
    st.pyplot(plt)


def plot_idade_ingressantes(df):
    bins = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    labels = ['16-20', '21-25', '26-30', '31-35', '36-40',
              '41-45', '46-50', '51-55', '56-60', '61-65', '66-70']
    df['Faixa_Etaria'] = pd.cut(
        df['IDADE_INGRESSO'], bins=bins, labels=labels, right=False)
    faixa_etaria_counts = df['Faixa_Etaria'].value_counts().sort_index()
    plt.figure(figsize=(12, 8))
    sns.barplot(x=faixa_etaria_counts.index, y=faixa_etaria_counts.values)
    plt.title('Quantidade de Ingressantes por Faixa Etária')
    plt.xlabel('Faixa Etária')
    plt.ylabel('Quantidade')
    plt.tight_layout()
    st.pyplot(plt)


def plot_top_10_naturalidade(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['NATURALIDADE'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['NATURALIDADE'].isin(top_10)],
                  y='NATURALIDADE', order=top_10)
    plt.title('Top 10 Naturalidades')
    plt.xlabel('Quantidade')
    plt.ylabel('Naturalidade')
    plt.tight_layout()
    st.pyplot(plt)


def plot_top_10_endereco(df):
    plt.figure(figsize=(10, 6))
    top_10 = df['CIDADE_ENDERECO'].value_counts().nlargest(10).index
    sns.countplot(data=df[df['CIDADE_ENDERECO'].isin(
        top_10)], y='CIDADE_ENDERECO', order=top_10)
    plt.title('Top 10 Endereços (Cidade)')
    plt.xlabel('Quantidade')
    plt.ylabel('Cidade')
    plt.tight_layout()
    st.pyplot(plt)


def calcular_matriz_transicao(df):
    transicoes = df.groupby(['CIDADE_ENDERECO', 'CAMPUS']
                            ).size().unstack(fill_value=0)

    stochastic_matrix = transicoes.div(transicoes.sum(axis=1), axis=0)

    return stochastic_matrix


def plot_ingressantes_por_curso_ano(df, cursos_selecionados):
    if not cursos_selecionados:
        cursos_selecionados = df['CURSO'].value_counts().nlargest(5).index
    df_cursos_ano = df[df['CURSO'].isin(cursos_selecionados)].groupby(
        ['ANO_INGRESSO', 'CURSO']).size().unstack().fillna(0)
    fig = px.line(df_cursos_ano, x=df_cursos_ano.index,
                  y=cursos_selecionados, markers=True)
    fig.update_layout(
        title='Evolução do Número de Ingressantes por Curso ao Longo dos Anos',
        xaxis_title='Ano de Ingresso',
        yaxis_title='Quantidade de Ingressantes',
        xaxis=dict(
            tickvals=df_cursos_ano.index,  # Define os valores dos ticks como os anos
            # Define os textos dos ticks como os anos
            ticktext=[str(year) for year in df_cursos_ano.index],
        ),
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_impacto_bonificacao(df):

    medicina_df = df[(df['CURSO'] == 'MEDICINA') & (
        df['CAMPUS'] == 'REITOR JOAQUIM AMAZONAS')]

    medicina_df['Beneficiario_Bonus'] = (medicina_df['UF_ENDERECO'] == 'PE') & (
        medicina_df['UF_NATURALIDADE'] == 'PE')

    total_medicina = len(medicina_df)
    qualificados = medicina_df['Beneficiario_Bonus'].sum()
    nao_qualificados = total_medicina - qualificados

    bonus_df = pd.DataFrame({
        'Status': ['Qualificado para Bônus', 'Não Qualificado'],
        'Quantidade': [qualificados, nao_qualificados]
    })

    fig = px.pie(bonus_df, values='Quantidade', names='Status',
                 title='Impacto do Bônus de Inclusão Regional no Curso de Medicina',
                 template='plotly_dark')
    fig.update_traces(textposition='inside',
                      textinfo='percent+label', insidetextfont=dict(size=20))
    fig.update_layout(width=350, height=350)

    st.plotly_chart(fig, use_container_width=True)


st.set_page_config(layout='wide',
                   page_title="Análise por campus")

st.title('Análise por Campus')

df = pd.read_json("./datasets/colect-data.json")

df['IDADE_INGRESSO'] = df['ANO_INGRESSO'] - df['ANO_NASC']

anos = ['Todos'] + df['ANO_INGRESSO'].unique().tolist()
semestres = ['Todos'] + df['SEMESTRE_INGRESSO'].unique().tolist()
campi = ['Todos'] + df['CAMPUS'].unique().tolist()

ano_selecionado = st.sidebar.selectbox('Selecione o Ano de Ingresso', anos)
semestre_selecionado = st.sidebar.selectbox(
    'Selecione o Semestre de Ingresso', semestres)
campus_selecionado = st.sidebar.selectbox('Selecione o Campus', campi)

df_filtered = df.copy()

if ano_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['ANO_INGRESSO'] == ano_selecionado]
if semestre_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['SEMESTRE_INGRESSO']
                              == semestre_selecionado]
if campus_selecionado != 'Todos':
    df_filtered = df_filtered[df_filtered['CAMPUS'] == campus_selecionado]

st.header('KPIs')
col1, col2 = st.columns(2)

col1.metric('Total de Ingressantes', len(df_filtered))

sexo_counts = df_filtered['SEXO'].value_counts(normalize=True) * 100
cota_counts = df_filtered['COTA'].value_counts(normalize=True) * 100

charts1, charts2 = st.columns(2)

with charts1:
    st.subheader('Proporção por Sexo')
    plot_sexo_counts(sexo_counts)

    st.subheader('Ingressantes por Ano e Semestre')
    plot_ingressantes_por_ano_semestre(df_filtered)

    st.subheader('Top 10 Cursos')
    plot_top_10_curso(df_filtered)

    st.subheader('Top 10 Naturalidades')
    plot_top_10_naturalidade(df_filtered)

with charts2:
    st.subheader('Proporção por Cotas')
    plot_cota_counts(cota_counts)

    st.subheader('Distribuição por Campus')
    plot_campus(df_filtered)

    st.subheader('Idades dos Ingressantes')
    plot_idade_ingressantes(df_filtered)

    st.subheader('Top 10 Endereços (Cidade)')
    plot_top_10_endereco(df_filtered)

todos_cursos = df['CURSO'].unique().tolist()

col3, col4 = st.columns(2)

with col3:
    cursos_selecionados = st.multiselect(
        'Selecione um ou mais Cursos para visualizar no gráfico abaixo', todos_cursos)

st.header('Evolução do Número de Ingressantes por Curso ao Longo dos Anos')
plot_ingressantes_por_curso_ano(df_filtered, cursos_selecionados)

st.header('Matriz Estocástica de Transição: Campus e Cidade de Endereço')
matriz_transicao = calcular_matriz_transicao(df_filtered)
st.write(matriz_transicao)

st.header('Impacto do Bônus de Inclusão Regional no Curso de Medicina')
plot_impacto_bonificacao(df_filtered)
