# --------------------------------------------------------------------------------------------------------------------- #
# Anotações
# --------------------------------------------------------------------------------------------------------------------- #
# ver dash: streamlit run python/streamlit/dash_completo.py

# --------------------------------------------------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------------------------------------------------- #

import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
from datetime import datetime

from path_planilha import *

st.set_page_config(layout="wide", page_title = 'Fluxo financeiro', page_icon = '🏠')

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
# Conteúdo da página
# --------------------------------------------------------------------------------------------------------------------- #

st.header('🏠 Fluxo financeiro')
st.markdown('')
st.markdown('##### Proporção de gastos por categoria ao longo do tempo')
st.markdown('')
tipo_grafico = st.selectbox('Tipo', ['Percentual', 'Valor'])
st.markdown('')

# start_time = st.slider(
#     "Selecionar intervalo de tempo",
#     value=(datetime(2023, 1, 1), datetime(2025, 12, 31)),
#     format="DD/MM/YYYY",
# )

# st.write("Intervalo de tempo", start_time)

barras_emplilhadas = df.copy()
barras_emplilhadas['mes_ano'] = barras_emplilhadas['mes'] + '/' + barras_emplilhadas['ano'].astype(str)
barras_emplilhadas['macro'] = np.where(barras_emplilhadas['macro'].isin(['streamings', 'estética', 'tarifas', 'contas', 'conhecimento']), 'outros', barras_emplilhadas['macro'])
barras_emplilhadas = barras_emplilhadas.groupby(['mes_ano', 'ano', 'mes_num', 'macro'])['valor'].sum().reset_index()
barras_emplilhadas['total_mes'] = barras_emplilhadas.groupby('mes_ano')['valor'].transform(sum)
barras_emplilhadas['pct'] = barras_emplilhadas['valor'] / barras_emplilhadas['total_mes']
barras_emplilhadas['macro'] = pd.Categorical(barras_emplilhadas['macro'],
                                             categories = ['casa', 'investimentos', 'saúde', 'transporte', 'social',
                                                           'eletrônicos', 'vestuário', 'alimentação', 'outros'],
                                             ordered = True)
barras_emplilhadas = barras_emplilhadas.sort_values(['macro', 'ano', 'mes_num', 'macro'])
barras_emplilhadas['text'] = barras_emplilhadas['valor'].apply(lambda x: sep_milhar(x) + ',' + str(round(x, 2)).split('.')[1].ljust(2, '0'))

dict_cores = {'investimentos':'#2d2d2d', 'casa':'#3E5461', 'saúde':'#5288db', 'alimentação':'#364D37',
                                 'social':'#B0BB9B', 'transporte':'#511012', 'eletrônicos':'#DFA03F', 'vestuário':'white', 'outros':'gray'}

if tipo_grafico == 'Percentual':
    eixo_y = 'pct'
    fmt = '.0%'
else:
    eixo_y = 'valor'
    fmt = '.0f'

fig = go.Figure(layout = dict(barcornerradius = 5))
for categoria in barras_emplilhadas['macro'].unique():
    df_tmp = barras_emplilhadas[barras_emplilhadas['macro'] == categoria]
    fig.add_trace(go.Bar(x = df_tmp['mes_ano'],
                  y = df_tmp[eixo_y],
                  name = categoria,
                  marker_color = dict_cores[categoria],
                  customdata = list(zip(df_tmp['macro'], df_tmp['text'], df_tmp['pct'])),
                  hovertemplate = '%{customdata[0]}<br>Mês: %{x}<br>Total: R$ %{customdata[1]}<br>Percentual: %{customdata[2]:.1%}<extra></extra>'))
    
fig.update_layout(height = 530, barmode = 'stack', plot_bgcolor = 'rgba(0, 0, 0, 0)', paper_bgcolor = 'rgba(0, 0, 0, 0)', margin=dict(l=0, r=0, t=0, b=0))
fig.update_yaxes(tickformat = fmt)
st.plotly_chart(fig)