# --------------------------------------------------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------------------------------------------------- #

import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go

from path_planilha import *

st.set_page_config(layout="wide", page_title = 'Despesas por categoria', page_icon = '📊')

# --------------------------------------------------------------------------------------------------------------------- #
# Carregar e tratar base de dados
# --------------------------------------------------------------------------------------------------------------------- #

@st.cache_data
def load_data():
    file_path = PATH_DESPESAS
    if not os.path.exists(file_path):
        st.error(f"Arquivo não encontrado: {file_path}")
        st.stop()
    return pd.read_excel(file_path, sheet_name = 'despesas')

df = load_data()
df = df[df['categoria'].notna()]
df = df[['categoria', 'valor', 'mes_num', 'mes', 'ano', 'macro']]
df['mes_num'] = df['mes_num'].astype(int)
df['ano'] = df['ano'].astype(int)

# --------------------------------------------------------------------------------------------------------------------- #
# Criar colunas para as listas suspensas
# --------------------------------------------------------------------------------------------------------------------- #

st.header('📊 Despesas por categoria')

# ano_selecionado = st.selectbox('Ano', anos)
# mes_selecionado = st.selectbox('Mês', meses)
# agrupamento_selecionado = st.selectbox('Agrupar categorias?', opcoes_agrupamento)
col1, col2, col3 = st.columns([1, 1, 1])  # 1: largura do menu, 2: largura do gráfico


# --------------------------------------------------------------------------------------------------------------------- #
# Menu de listas suspensas
# --------------------------------------------------------------------------------------------------------------------- #

# Listas suspensas para seleção
anos = df['ano'].unique()
meses = list(df['mes'].unique())
meses.insert(0, 'todos os meses')
opcoes_agrupamento = ['Sim', 'Não']

with col1:
    ano_selecionado = st.selectbox('Ano', anos)
with col2:
    mes_selecionado = st.selectbox('Mês', meses)
with col3:
    agrupamento_selecionado = st.selectbox('Agrupar categorias?', opcoes_agrupamento)