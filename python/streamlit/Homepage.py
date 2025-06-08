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

from path_planilha import *

st.set_page_config(layout="wide", page_title = 'Fluxo financeiro', page_icon = '🏠')

# --------------------------------------------------------------------------------------------------------------------- #
# Conteúdo da página
# --------------------------------------------------------------------------------------------------------------------- #

st.header('🏠 Fluxo financeiro')

col1, col2 = st.columns(2)
# if col1.button("Plain button", use_container_width=True):
#     left.markdown("You clicked the plain button.")
# if middle.button("Emoji button", icon="😃", use_container_width=True):
#     middle.markdown("You clicked the emoji button.")
# if right.button("Material button", icon=":material/mood:", use_container_width=True):
#     right.markdown("You clicked the Material button.")

#     st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")


with col1:
    st.markdown('')
    st.link_button("📊 Despesas por categoria", "Despesas_por_categoria", use_container_width = True)
    st.link_button("📆 Despesas mensais", "Despesas_mensais", use_container_width = True)

with col2:
    st.markdown('')
    st.link_button("📈 Microcategorias no tempo", "Microcategorias_no_tempo", use_container_width = True)
    st.link_button("💰 Evolução dos investimentos", "Evolução_dos_investimentos", use_container_width = True)