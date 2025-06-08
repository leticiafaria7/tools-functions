# --------------------------------------------------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------------------------------------------------- #

import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go

from path_planilha import *

st.set_page_config(layout="wide", page_title = 'Evolução dos investimentos', page_icon = '💰')

# --------------------------------------------------------------------------------------------------------------------- #
# Carregar e tratar base de dados
# --------------------------------------------------------------------------------------------------------------------- #

st.header('💰 Evolução dos investimentos')