import streamlit as st


def navbar():
    no_sidebar_style = """
        <style>
            div[data-testid="stSidebarNav"] {display: none;}
        </style>
    """

    st.markdown(no_sidebar_style, unsafe_allow_html=True)

    st.sidebar.image('./images/logo-ufpe.png', use_column_width=True)

    st.sidebar.divider()

    st.sidebar.page_link("./main.py", label="Informações", icon="📚")
    st.sidebar.page_link("./pages/campus.py",
                         label="Análise por Campus", icon="🏫")
    st.sidebar.page_link("./pages/cidades.py",
                         label="Análise por Cidades", icon="🏙️")
    st.sidebar.page_link(
        "./pages/mapa.py", label="Mapa de Distribuição", icon="🌎")

    st.sidebar.divider()
