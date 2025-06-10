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

def sep_milhar(num, casas_decimais = 0):
    return f"{num:,.{casas_decimais}f}".replace(",", ".")

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

row1 = st.columns([1, 2, 3])
row2 = st.columns([1, 1])

# --------------------------------------------------------------------------------------------------------------------- #
# Menu de listas suspensas
# --------------------------------------------------------------------------------------------------------------------- #

# Listas suspensas para seleção
anos = df['ano'].unique()
meses = list(df['mes'].unique())
meses.insert(0, 'todos os meses')


with row1[0]:
    ano_selecionado = st.selectbox('Ano', anos)
with row1[1]:
    mes_selecionado = st.selectbox('Mês', meses)
with row1[2]:
    if mes_selecionado == 'todos os meses':
        categorias = df[(df['ano'] == ano_selecionado)]['macro'].unique()
    else:
        categorias = df[(df['ano'] == ano_selecionado) & (df['mes'] == mes_selecionado)]['macro'].unique()
    macro_selecionada = st.selectbox('Macrocategoria', categorias)

# --------------------------------------------------------------------------------------------------------------------- #
# Bases de dados tratadas
# --------------------------------------------------------------------------------------------------------------------- #

# Filtrar os dados com base na seleção do usuário
if mes_selecionado == 'todos os meses':
    dados_filtrados = df[(df['ano'] == ano_selecionado)]
    dados_filtrados_categoria = df[(df['ano'] == ano_selecionado) & (df['macro'] == macro_selecionada)]
else:
    dados_filtrados = df[(df['ano'] == ano_selecionado) & (df['mes'] == mes_selecionado)]
    dados_filtrados_categoria = df[(df['ano'] == ano_selecionado) & (df['mes'] == mes_selecionado) & (df['macro'] == macro_selecionada)]

# para gráfico 1
dados_filtrados = dados_filtrados.groupby(['macro'])['valor'].sum().reset_index()
dados_filtrados['total'] = dados_filtrados['valor'].sum()
dados_filtrados['pct'] = round(dados_filtrados['valor'] * 100 / dados_filtrados['total'], 1)
dados_filtrados = dados_filtrados.sort_values(['valor'], ascending = [True])
dados_filtrados['valor'] = dados_filtrados['valor'].round(2)
dados_filtrados['valor_tratado'] = dados_filtrados['valor'].apply(lambda x: sep_milhar(x) + ',' + str(x).split('.')[1].ljust(2, '0'))
dados_filtrados['text'] = '<b>R$ ' + dados_filtrados['valor_tratado'].round(2).astype(str) + '</b> (' + dados_filtrados['pct'].astype(str) + '%)'

# para gráfico 2
dados_filtrados_categoria = dados_filtrados_categoria.groupby(['categoria'])['valor'].sum().reset_index()
dados_filtrados_categoria['total'] = dados_filtrados_categoria['valor'].sum()
dados_filtrados_categoria['pct'] = round(dados_filtrados_categoria['valor'] * 100 / dados_filtrados_categoria['total'], 1)
dados_filtrados_categoria = dados_filtrados_categoria.sort_values(['valor'], ascending = [True])
dados_filtrados_categoria['valor'] = dados_filtrados_categoria['valor'].round(2)
dados_filtrados_categoria['valor_tratado'] = dados_filtrados_categoria['valor'].apply(lambda x: sep_milhar(x) + ',' + str(x).split('.')[1].ljust(2, '0'))
dados_filtrados_categoria['text'] = '<b>R$ ' + dados_filtrados_categoria['valor_tratado'].round(2).astype(str) + '</b> (' + dados_filtrados_categoria['pct'].astype(str) + '%)'

# para gráfico 3
dados_filtrados_linhas = df[(df['ano'] == ano_selecionado) & (df['macro'] == macro_selecionada)]
dados_filtrados_linhas = df[['mes_num', 'mes']].drop_duplicates().reset_index(drop = True)\
        .merge(dados_filtrados_linhas.groupby(['mes_num', 'mes'])['valor'].sum().reset_index(), on = ['mes_num', 'mes'], how = 'left').fillna(0)

# --------------------------------------------------------------------------------------------------------------------- #
# Gráficos
# --------------------------------------------------------------------------------------------------------------------- #

with row2[0]:
    # Função para plotar o gráfico
    st.text("")
    st.text("")
    st.markdown('##### Despesas por macrocategoria')
    def plotar_grafico_1(df):

        fig = go.Figure(layout = dict(barcornerradius = 5))
        fig.add_trace(go.Bar(x = df['valor'], 
                            y = df['macro'],
                            orientation = 'h',
                            width = 0.6,
                            textposition = 'outside',
                            marker = dict(color = ['brown'] * df.shape[0]),
                            customdata = list(zip(df['pct'], df['valor_tratado'])),
                            hovertemplate = '%{y}<br><br>Total gasto: R$ %{customdata[1]}<br>Proporção: %{customdata[0]}%<extra></extra>',
                            text = df['text']))
        fig.add_shape(type = 'line', x0 = 0, x1 = 0, y0 = -1, y1 = df.shape[0], line = dict(width = 0.8, color = 'lightgray'))
        fig.update_layout(plot_bgcolor = 'rgba(0, 0, 0, 0)', paper_bgcolor = 'rgba(0, 0, 0, 0)', height = 550, width = 800, 
                          margin=dict(l=0, r=0, t=0, b=0))
        fig.update_xaxes(range = [0, df.valor.max() * 1.3])
        
        st.plotly_chart(fig)

    # Plotar o gráfico com base na opção de agrupamento
    plotar_grafico_1(dados_filtrados)

with row2[1]:
    st.text("")
    st.text("")
    st.markdown('##### Subcategorias (selecionar macro)')
    def plotar_grafico_2(df):

        fig = go.Figure(layout = dict(barcornerradius = 5))
        fig.add_trace(go.Bar(x = df['valor'], 
                            y = df['categoria'],
                            orientation = 'h',
                            width = 0.6,
                            textposition = 'outside',
                            marker = dict(color = ['brown'] * df.shape[0]),
                            customdata = list(zip(df['pct'], df['valor_tratado'])),
                            hovertemplate = '%{y}<br><br>Total gasto: R$ %{customdata[1]}<br>Proporção: %{customdata[0]}%<extra></extra>',
                            text = df['text']))
        fig.add_shape(type = 'line', x0 = 0, x1 = 0, y0 = -1, y1 = df.shape[0], line = dict(width = 0.8, color = 'lightgray'))
        fig.update_layout(plot_bgcolor = 'rgba(0, 0, 0, 0)', paper_bgcolor = 'rgba(0, 0, 0, 0)',  height = 250, width = 800,
                          margin=dict(l=0, r=0, t=0, b=0))
        fig.update_xaxes(range = [0, df.valor.max() * 1.3])
        st.plotly_chart(fig)

    plotar_grafico_2(dados_filtrados_categoria)

    st.text("")
    st.markdown(f'##### Gastos mensais da macro em {ano_selecionado}')
    def plotar_grafico_3(df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df['mes'],
                              y = df['valor'],
                            #   marker = dict(color = ['brown'] * 12),
                              line = dict(color = 'brown'),
                              hovertemplate = 'Mês: %{x}<br><br>Total gasto: R$ %{y}<extra></extra>'))
        fig.add_shape(type = 'line', x0 = 0, x1 = 12, y0 = 0, y1 = 0, line = dict(width = 0.8, color = 'lightgray'))
        fig.update_layout(plot_bgcolor = 'rgba(0, 0, 0, 0)', paper_bgcolor = 'rgba(0, 0, 0, 0)', 
                        height = 250, width = 800,
                        margin=dict(l=0, r=0, t=0, b=0))
        fig.update_yaxes(range = [-df.valor.min() * 0.1, df.valor.max() * 1.3])
        st.plotly_chart(fig)

    plotar_grafico_3(dados_filtrados_linhas)
    