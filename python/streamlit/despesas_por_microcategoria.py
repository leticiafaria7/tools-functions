# proximos passos:
# adicionar categoria "todos" no mês
# adicionar percentual
# adicionar legenda
# adicionar outra visualização para cobrir o percentual
# adicionar insights de onde dá para reduzir custos


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go

from path_planilha import *

# Carregar a base de dados    
@st.cache_data
def load_data():
    # file_path = 'base_despesas.csv'
    # if not os.path.exists(file_path):
    #     st.error(f"Arquivo não encontrado: {file_path}")
    #     st.stop()
    return pd.read_excel(PATH_DESPESAS, sheet_name = 'despesas')

df = load_data()
df = df[df['categoria'].notna()]
df = df[['categoria', 'valor', 'mes_num', 'mes', 'ano', 'macro']]
# df['valor'] = df['valor'].astype(str).apply(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.')).astype(float)
df['mes_num'] = df['mes_num'].astype(int)
df['ano'] = df['ano'].astype(int)

# Criação das colunas para a interface
st.subheader('Despesas por microcategoria')
col1, col2 = st.columns([1, 2])  # 1: largura do menu, 2: largura do gráfico

with col1:
    # Listas suspensas para seleção
    anos = df['ano'].unique()
    meses = df['mes'].unique()
    opcoes_agrupamento = ['Sim', 'Não']

    ano_selecionado = st.selectbox('Selecione o ano', anos)
    mes_selecionado = st.selectbox('Selecione o mês', meses)
    agrupamento_selecionado = st.selectbox('Agrupar categorias?', opcoes_agrupamento)

# Filtrar os dados com base na seleção do usuário
dados_filtrados = df[(df['ano'] == ano_selecionado) & (df['mes'] == mes_selecionado)].copy()
dados_filtrados = dados_filtrados.groupby(['macro', 'categoria']).agg({'valor':'sum'}).reset_index()


with col2:
    # Função para plotar o gráfico
    def plotar_grafico(df, agrupar):

        if agrupar == 'Sim':
            df = df.sort_values(['macro', 'valor'], ascending = [False, True])
        else:
            df = df.sort_values(['valor'], ascending = [True])

        colors = {
            'alimentação': '#d4d4d4', 
            'casa': '#005f73',
            'conhecimento': '#0a9396',
            'contas': '#94d2bd',
            'eletrônicos': '#e9d8a6',
            'estética': '#ee9b00',
            'investimentos': '#ca6702',
            'saúde': '#bb3e03',
            'social': '#ae2012',
            'streamings': '#9b2226',
            'tarifas': '#5288db',
            'transporte': '#ac34ae',
            'vestuário': '#dac0ac'
        }

        fig = go.Figure(layout = dict(barcornerradius = 5))

        fig.add_trace(
            go.Bar(
                x = df['valor'],
                y = df['categoria'],
                orientation = 'h',
                width = 0.6,
                marker=dict(
                    color=[colors[m] for m in df['macro']]
                ),
                text=df['valor'].apply(lambda x: f'R$ {x:,.2f}'),
                textposition=None,
                hovertemplate='Valor: R$ %{x:,.2f}<br>Macro: %{customdata}<extra></extra>',
                customdata=df['macro']
            )
        )

        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                           'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

        fig.update_layout(width=1200, 
                          height=700,
                          margin=dict(l=0, r=0, t=0, b=0))
        
        st.plotly_chart(fig)

    # Plotar o gráfico com base na opção de agrupamento
    plotar_grafico(dados_filtrados, agrupamento_selecionado)
