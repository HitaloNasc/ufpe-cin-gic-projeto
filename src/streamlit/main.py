import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout='wide',
                   page_title="Ingressantes SISU UFPE")

st.title("Sobre o trabalho")

st.header("Introdução")

st.markdown(
    '<div style="text-align: justify; margin-bottom: 20px;">'
    'O objetivo deste projeto é realizar uma análise abrangente dos dados dos ingressantes na Universidade Federal de Pernambuco (UFPE) no período de 2020 a 2024. Focamos em diversas informações cruciais, como a origem dos aprovados, o campus de destino, os cursos escolhidos, e a utilização de cotas, incluindo os diferentes tipos de cotas disponíveis. Para isso, empregaremos dados detalhados e ferramentas de análise avançadas para obter insights precisos e significativos.'
    '</div>'
    '<div style="text-align: justify; margin-bottom: 20px;">'
    'Nossa análise pretende identificar padrões e tendências que possam fornecer uma compreensão mais profunda sobre o perfil dos estudantes que ingressaram na UFPE nesses anos. Consideramos fatores como a distribuição geográfica dos ingressantes, a escolha dos campi e dos cursos, bem como a influência das políticas de cotas na composição do corpo discente. Ao explorar essas dimensões, esperamos revelar elementos que possam auxiliar na formulação de políticas educacionais e na melhoria dos processos de admissão da universidade.'
    '</div>'
    '<div style="text-align: justify; margin-bottom: 20px;">'
    'Utilizaremos a ferramenta Streamlit para apresentar a análise de forma interativa e visualmente atraente. As bibliotecas Python pandas, openpyxl, matplotlib, seaborn, pymongo e python-dotenv serão empregadas para a manipulação dos dados, criação de visualizações, e gerenciamento de ambientes. Com essas metodologias e ferramentas robustas, pretendemos criar uma visão detalhada e integrada dos ingressantes na UFPE, contribuindo para uma gestão mais eficaz e inclusiva da educação superior.'
    '</div>',
    unsafe_allow_html=True
)

st.header("Metodologia")

st.markdown(
    '<div style="text-align: justify; margin-bottom: 20px;">'
    'A ferramenta escolhida para este projeto foi o Streamlit por diversos motivos. Primeiramente, alguns membros do grupo já possuem experiência com a ferramenta, o que facilita a implementação. Além disso, por ser uma ferramenta gratuita, o Streamlit se torna uma opção econômica e inclusiva. Outro fator importante é que Streamlit é baseado em Python, uma linguagem que todos os integrantes dominam, reduzindo significativamente a curva de aprendizagem.'
    '</div>'
    '<div style="text-align: justify; margin-bottom: 20px;">'
    'Os dados utilizados neste projeto foram coletados a partir dos registros de ingressantes da UFPE, abrangendo os anos de 2020 a 2024, porém não foram disponibilizados os dados dos semestres 2021.2 e 2024.2. As informações incluídas nos dados são: origem dos aprovados, campus de destino, cursos escolhidos, e a utilização de cotas, incluindo os diferentes tipos de cotas. A limpeza e organização dos dados foram etapas cruciais para garantir a confiabilidade e a precisão das análises. Utilizamos a biblioteca pandas para manipulação dos dados, removendo linhas com informações em branco e excluindo colunas que não eram relevantes para a análise proposta. A biblioteca openpyxl foi utilizada para trabalhar com arquivos csv, facilitando a importação e exportação de dados.'
    '</div>'
    '</div>'
    '<div style="text-align: justify; margin-bottom: 20px;">'
    'Para a análise dos dados, utilizamos as bibliotecas matplotlib e seaborn, que nos permitiram criar visualizações detalhadas e intuitivas. Essas visualizações foram essenciais para identificar padrões e tendências nos dados, como a distribuição geográfica dos ingressantes, a escolha dos campi e cursos, e a influência das políticas de cotas.'
    '</div>',
    unsafe_allow_html=True
)


pessoas = [
    {"nome": "Douglas Araújo", "github_url": "https://github.com/thedouglasaraujo"},
    {"nome": "Hallan Ângelo", "github_url": "https://github.com/hallanangelo"},
    {"nome": "Hítalo Nascimento", "github_url": "https://github.com/HitaloNasc"},
    {"nome": "Ingrid Freire", "github_url": "https://github.com/ingridfsl"},
    {"nome": "Katharian Abrahel", "github_url": "https://github.com/katharianabrahel"}
]

st.write("\n\n")
st.markdown("---")
st.write("Desenvolvido por:")

cols = st.columns(len(pessoas))

for col, pessoa in zip(cols, pessoas):
    with col:
        st.markdown(
            f"""
            <a href="{pessoa['github_url']}" style='text-decoration: none;'>
                <div style='display: flex; flex-direction: column; align-items: center;'>
                    <img src="{pessoa['github_url']}.png" width="150" height="150" style='border-radius: 50%;'><br>
                    <span style='font-size: 20px; color: #0068c9;'>{pessoa['nome']}</span>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )