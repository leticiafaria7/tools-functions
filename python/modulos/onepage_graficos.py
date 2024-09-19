# --------------------------------------------------------------------------------------------------------------------------------------------- #
# Bibliotecas
# --------------------------------------------------------------------------------------------------------------------------------------------- #

import pandas as pd
import numpy as np
import sys, os
from os import walk

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings("ignore")

from IPython.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))

# --------------------------------------------------------------------------------------------------------------------------------------------- #
# Função para gerar o onepage
# --------------------------------------------------------------------------------------------------------------------------------------------- #

def gerar_dash(base_grafico_1_1: pd.DataFrame, base_grafico_1_2: pd.DataFrame, 
               base_grafico_2_1: pd.DataFrame, base_grafico_2_2: pd.DataFrame, base_grafico_2_3: pd.DataFrame, 
               base_grafico_3_1: pd.DataFrame, base_grafico_3_2: pd.DataFrame, base_grafico_3_3: pd.DataFrame, 
               base_grafico_4: pd.DataFrame, base_grafico_5: pd.DataFrame,
               marca: str, produto: str, cluster: str, n_competidores: int,
               path_entrega_final: str,
               axis_title_size: int = 12, tick_font_size: int = 9, 
               show_fig: bool = True, save_fig: bool = False):

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # Estrutura do gráfico
    # ----------------------------------------------------------------------------------------------------------------------------------------- #

    cores = ['#E63946', '#FDCA40', '#2176FF', '#457B9D', '#1D3557', '#FF4C24', '#A8DADC']

    specs = [[{"colspan":3}, None, None, {"colspan":3}, None, None],
             [{"colspan":2, 'secondary_y': True}, None, {"colspan":2, 'secondary_y': True}, None, {"colspan":2, 'secondary_y': True}, None],
             [{"colspan":2, 'secondary_y': True}, None, {"colspan":2}, None, {"colspan":2}, None],
             [{"colspan":6}, None, None, None, None, None]]

    row_comp = [{"colspan":3, 'secondary_y': True}, None, None, {"colspan":3}, None, None]
    n_rows = 4 + n_competidores

    fig = make_subplots(
        rows = n_rows, cols = 6,
        specs = specs + [row_comp for _ in range(n_competidores)],
        print_grid = False,
        horizontal_spacing = (0.6 / 5),
        vertical_spacing = (0.3 / 5)
    )

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # 1. Pricing points
    # ----------------------------------------------------------------------------------------------------------------------------------------- #

    fig.add_trace(go.Scatter(x = base_grafico_1_1['vlr_item'],
                            y = base_grafico_1_1['qtd_item'],
                            mode = 'markers',
                            hovertemplate = 'Demanda: %{y:.0f}<br>Preço: R$ %{x:.2f}<extra></extra>',
                            name = 'Dados brutos',
                            marker_color = cores[2],
                            legendgroup = 'pricing_points',
                            legendgrouptitle_text = '1. Pricing points'),
                            row = 1, col = 1)

    fig.add_trace(go.Scatter(x = base_grafico_1_2['preco'],
                            y = base_grafico_1_2['demanda'],
                            hovertemplate = 'Demanda: %{y:.0f}<br>Preço: R$ %{x:.2f}<extra></extra>',
                            name = 'Agrupamento por janelas móveis',
                            mode = 'markers',
                            marker_color = cores[2],
                            legendgroup = 'pricing_points',
                            legendgrouptitle_text = '1. Pricing points'),
                            row = 1, col = 4)

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # 2. Sazonalidade
    # ----------------------------------------------------------------------------------------------------------------------------------------- #

    # Mês -------------------------------------------------------------------------

    fig.add_trace(go.Bar(x = base_grafico_2_1['mes'].astype(str),
                        y = base_grafico_2_1['qtd_item'],
                        name = 'Número de atendimentos<br>(real)',
                        marker_color = cores[2],
                        legendgroup = 'sazonalidade',
                        legendgrouptitle_text = '2. Sazonalidade',
                        hovertemplate = 'Mês: %{x}<br>Demanda real: %{y}<extra></extra>'),
                        secondary_y = False,
                        row = 2, col = 1)

    fig.add_trace(go.Bar(x = base_grafico_2_1['mes'].astype(str),
                        y = base_grafico_2_1['qtd_item_deseasonalized'],
                        name = 'Número de atendimentos<br>(sem sazonalidade)',
                        marker_color = cores[0],
                        legendgroup = 'sazonalidade',
                        legendgrouptitle_text = '2. Sazonalidade',
                        hovertemplate = 'Mês: %{x}<br>Demanda dessazonalizada: %{y}<extra></extra>'),
                        secondary_y = False,
                        row = 2, col = 1)

    fig.add_trace(go.Scatter(x = base_grafico_2_1['mes'].astype(str),
                            y = base_grafico_2_1['receita'],
                            name = 'Receita',
                            mode = 'lines',
                            marker_color = cores[1],
                            legendgroup = 'sazonalidade',
                            legendgrouptitle_text = '2. Sazonalidade',
                            hovertemplate = 'Mês: %{x}<br>Receita: R$ %{y:.2f}<extra></extra>'),
                            secondary_y = True,
                            row = 2, col = 1)

    # Dia da semana -------------------------------------------------------------------------

    fig.add_trace(go.Bar(x = base_grafico_2_2['dia_da_semana'],
                        y = base_grafico_2_2['qtd_item'],
                        name = 'Número de atendimentos<br>(sem sazonalidade)',
                        marker_color = cores[0],
                        legendgroup = 'sazonalidade',
                        legendgrouptitle_text = '2. Sazonalidade',
                        hovertemplate = 'Dia da semana: %{x}<br>Demanda real: %{y}<extra></extra>'),
                        secondary_y = False,
                        row = 2, col = 3)

    fig.add_trace(go.Scatter(x = base_grafico_2_2['dia_da_semana'],
                            y = base_grafico_2_2['receita'],
                            name = 'Receita',
                            mode = 'lines',
                            marker_color = cores[1],
                            legendgroup = 'sazonalidade',
                            legendgrouptitle_text = '2. Sazonalidade',
                            hovertemplate = 'Dia da semana: %{x}<br>Receita: R$ %{y:.2f}<extra></extra>'),
                            secondary_y = True,
                            row = 2, col = 3)

    # Horário -------------------------------------------------------------------------------

    fig.add_trace(go.Bar(x = base_grafico_2_3['faixas_horario'],
                        y = base_grafico_2_3['qtd_item'],
                        name = 'Número de atendimentos<br>(sem sazonalidade)',
                        marker_color = cores[0],
                        legendgroup = 'sazonalidade',
                        legendgrouptitle_text = '2. Sazonalidade',
                        hovertemplate = 'Faixa de horário: %{x}h<br>Demanda real: %{y}<extra></extra>'),
                        secondary_y = False,
                        row = 2, col = 5)

    fig.add_trace(go.Scatter(x = base_grafico_2_3['faixas_horario'],
                            y = base_grafico_2_3['receita'],
                            name = 'Receita',
                            mode = 'lines',
                            marker_color = cores[1],
                            legendgroup = 'sazonalidade',
                            legendgrouptitle_text = '2. Sazonalidade',
                            hovertemplate = 'Faixa de horário: %{x}h<br>Receita: R$ %{y:.2f}<extra></extra>'),
                            secondary_y = True,
                            row = 2, col = 5)

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # 3. Elasticidade
    # ----------------------------------------------------------------------------------------------------------------------------------------- #

    # gráfico 1 -------------------------------------------------------------------------

    fig.add_trace(go.Bar(x = base_grafico_3_1['mes'].astype(str),
                        y = base_grafico_3_1['demanda_total'],
                        name = 'Demanda',
                        marker_color = cores[6],
                        legendgroup = 'elasticidade',
                        legendgrouptitle_text = '3. Elasticidade',
                        hovertemplate = 'Mês: %{x}<br>Demanda total: %{y}<extra></extra>'),
                        secondary_y=False,
                        row = 3, col = 1)

    fig.add_trace(go.Scatter(x = base_grafico_3_1['mes'].astype(str),
                            y = base_grafico_3_1['preco_max'],
                            name = 'Preço máximo',
                            mode = 'lines',
                            marker_color = cores[4],
                            legendgroup = 'elasticidade',
                            legendgrouptitle_text = '3. Elasticidade',
                            hovertemplate = 'Mês: %{x}<br>Preço máximo: R$ %{y:.2f}<extra></extra>'),
                            secondary_y=True,
                            row = 3, col = 1)

    fig.add_trace(go.Scatter(x = base_grafico_3_1['mes'].astype(str),
                            y = base_grafico_3_1['preco_mediano'],
                            name = 'Preço mediano',
                            mode = 'lines',
                            marker_color = cores[5],
                            legendgroup = 'elasticidade',
                            legendgrouptitle_text = '3. Elasticidade',
                            hovertemplate = 'Mês: %{x}<br>Preço mediano: R$ %{y:.2f}<extra></extra>'),
                            secondary_y=True,
                            row = 3, col = 1)

    # gráfico 2 -------------------------------------------------------------------------

    fig.add_trace(go.Scatter(x = base_grafico_3_2['price'],
                            y = base_grafico_3_2['qtd'],
                            mode = 'markers',
                            name = 'Preço x demanda',
                            marker_color = cores[5],
                            legendgroup = 'elasticidade',
                            legendgrouptitle_text = '3. Elasticidade',
                            hovertemplate = 'Preço: R$ %{x:.2f}<br>Demanda: %{y}<extra></extra>'),
                            row = 3, col = 3)

    # gráfico 3 -------------------------------------------------------------------------------
    
    if base_grafico_3_3.shape[0] > 0:
        base_grafico_3_3['color'] = np.where((base_grafico_3_3.produto == produto) &
                                             (base_grafico_3_3.cluster_sugerido == cluster),
                                             cores[5], 'gray')
        base_grafico_3_3['opacity'] = np.where((base_grafico_3_3.produto == produto) &
                                               (base_grafico_3_3.cluster_sugerido == cluster),
                                               1, 0.5)
        base_grafico_3_3 = base_grafico_3_3.sort_values('opacity')
    else:
        base_grafico_3_3['color'] = None
        base_grafico_3_3['opacity'] = np.nan
    
    
    fig.add_trace(go.Scatter(x = base_grafico_3_3['coef_variacao_preco'],
                             y = base_grafico_3_3['coef_variacao_demanda'],
                             name = 'Outros produtos',
                             mode = 'markers',
                             marker_color = base_grafico_3_3['color'],
                             marker_opacity = base_grafico_3_3['opacity'],
                             legendgroup = 'elasticidade',
                             legendgrouptitle_text = '3. Elasticidade',
                             customdata = base_grafico_3_3['produto'],
                             hovertemplate = '%{customdata}<br>Coef. variação preço: %{x:.2f}<br>Coef. variação demanda: %{y:.2f}<extra></extra>'),
                             row = 3, col = 5)

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # 4. Performance histórica
    # ----------------------------------------------------------------------------------------------------------------------------------------- #

    fig.add_trace(go.Scatter(x = base_grafico_4['preco'], 
                             y = base_grafico_4['receita'], 
                             name = 'Performance histórica',
                             line_shape='spline',
                             marker_color = cores[1],
                             legendgroup = 'performance_historica',
                             legendgrouptitle_text = '4. Performance Histórica',
                             hovertemplate = 'Preço: R$ %{x:.2f}<br>Receita: R$ %{y:.2f}<extra></extra>'),
                             row = 4, col = 1)

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # 5. Competitividade
    # ----------------------------------------------------------------------------------------------------------------------------------------- #

    for idx, competidor in enumerate(base_grafico_5['empresa_marca'].unique()):

        # gráficos da esquerda -----------------------------------------------------------------------------------------------

        fig.add_trace(go.Scatter(x = base_grafico_5[base_grafico_5['empresa_marca'] == competidor]['mes'], 
                                y = base_grafico_5[base_grafico_5['empresa_marca'] == competidor].valor_competidores, 
                                mode = 'lines',
                                name = competidor,
                                customdata = base_grafico_5[base_grafico_5['empresa_marca'] == competidor]['empresa_marca'],
                                hovertemplate = '%{customdata}<br><br>Preço: R$ %{y:.2f}<br>Mês: %{x}<extra></extra>',
                                marker_color = cores[0],
                                legendgroup = 'dados_competidor',
                                legendgrouptitle_text = '5. Competitividade'),
                                row = (idx + 5), col = 1)

        fig.add_trace(go.Scatter(x = base_grafico_5[base_grafico_5['empresa_marca'] == competidor]['mes'], 
                                y = base_grafico_5[base_grafico_5['empresa_marca'] == competidor].valor_dasa, 
                                mode = 'lines',
                                name = 'Dasa - Preço mediano',
                                customdata = base_grafico_5[base_grafico_5['empresa_marca'] == competidor]['marca'],
                                hovertemplate = '%{customdata}<br><br>Preço: R$ %{y:.2f}<br>Mês: %{x}<extra></extra>',
                                marker_color = cores[2],
                                legendgroup = 'dados_competidor',
                                legendgrouptitle_text = '5. Competitividade'), 
                                row = (idx + 5), col = 1)
        
        fig.update_xaxes(title_text = 'Mês', row = (idx + 5), col = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(title_text = f'Preço mediano<br>{competidor}', row = (idx + 5), col = 1, secondary_y = False, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

        # gráficos da direita -----------------------------------------------------------------------------------------------

        fig.add_trace(go.Scatter(x = base_grafico_5[base_grafico_5['empresa_marca'] == competidor].diff_preco, 
                                y = base_grafico_5[base_grafico_5['empresa_marca'] == competidor].qtd_item, 
                                mode = 'markers',
                                customdata = base_grafico_5[base_grafico_5['empresa_marca'] == competidor]['empresa_marca'],
                                hovertemplate = '%{customdata}<br><br>Diferença de preço: R$ %{x:.2f}<br>Demanda: %{y}<extra></extra>',
                                name = competidor,
                                marker_color = cores[0],
                                legendgroup = 'dados_competidor',
                                legendgrouptitle_text = '5. Competitividade'), 
                                row = (idx + 5), col = 4)
        
        fig.update_xaxes(title_text = 'Diferença de preço', row = (idx + 5), col = 4, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(title_text = f'Demanda<br>{competidor}', row = (idx + 5), col = 4, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # Layout updates
    # ----------------------------------------------------------------------------------------------------------------------------------------- #

    # 1. Pricing points - row 1 ---------------------------------------------------------------------------------------------------

    fig.update_xaxes(title_text = 'Preço', row = 1, col = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_xaxes(title_text = 'Preço', row = 1, col = 4, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    fig.update_yaxes(title_text = 'Demanda', row = 1, col = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), 
                    range = [-(0.02 * base_grafico_1_1['qtd_item'].max()), 
                            1.1 * base_grafico_1_1['qtd_item'].max()], gridcolor='rgba(0,0,0,0.1)')

    fig.update_yaxes(title_text = 'Demanda', row = 1, col = 4,  title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), 
                    range = [-(0.02 * base_grafico_1_2['demanda'].max()), 
                            1.1 * base_grafico_1_2['demanda'].max()], gridcolor='rgba(0,0,0,0.1)')

    # 2. Sazonalidade - row 2 ---------------------------------------------------------------------------------------------------

    fig.update_xaxes(tickangle = 315, row = 2, col = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_xaxes(tickangle = 315, row = 2, col = 3, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_xaxes(tickangle = 0, row = 2, col = 5, dtick = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    fig.update_yaxes(title_text = 'Receita', row = 2, col = 1, secondary_y = True, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text = 'Receita', row = 2, col = 3, secondary_y = True, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text = 'Receita', row = 2, col = 5, secondary_y = True, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    fig.update_yaxes(title_text = 'Atendimentos', row = 2, col = 1, secondary_y = False, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text = 'Atendimentos', row = 2, col = 3, secondary_y = False, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text = 'Atendimentos', row = 2, col = 5, secondary_y = False, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    # 3. Elasticidade - row 3 ---------------------------------------------------------------------------------------------------

    fig.update_xaxes(title_text = '', tickangle = 315, row = 3, col = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_xaxes(title_text = 'Preço', tickangle = 315, row = 3, col = 3, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_xaxes(title_text = 'Coef. variação preço', tickangle = 0, row = 3, col = 5, dtick = 0.1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    fig.update_yaxes(title_text = 'Preço', row = 3, col = 1, secondary_y = True, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    fig.update_yaxes(title_text = 'Demanda', row = 3, col = 1, secondary_y = False, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text = 'Volume', row = 3, col = 3, secondary_y = False, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text = 'Coef. variação demanda', row = 3, col = 5, secondary_y = False, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), dtick = 0.25, gridcolor='rgba(0,0,0,0.1)')

    # 4. Performance histórica - row 4 ---------------------------------------------------------------------------------------------------

    fig.update_xaxes(title_text = 'Preço', row = 4, col = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')
    fig.update_yaxes(title_text = 'Receita', row = 4, col = 1, title_font = {"size": axis_title_size}, tickfont = dict(size = tick_font_size), gridcolor='rgba(0,0,0,0.1)')

    # 5. Competitividade - rows 5 em diante -----------------------------------------------------------------------------------------------

    # updates no loop

    # Parâmetros de acordo com o número de competidores -----------------------------------------------------------------------------------

    if n_competidores == 3:
        positions = {'height': 2000, 'pos_y1': 1.015, 'pos_y2': 0.875, 'pos_y3': 0.720, 'pos_y4': 0.560, 'pos_y5': 0.430}

    if n_competidores == 4:
        positions = {'height': 2200, 'pos_y1': 1.015, 'pos_y2': 0.890, 'pos_y3': 0.755, 'pos_y4': 0.610, 'pos_y5': 0.490}

    if n_competidores == 6:
        positions = {'height': 2600, 'pos_y1': 1.015, 'pos_y2': 0.920, 'pos_y3': 0.810, 'pos_y4': 0.700, 'pos_y5': 0.600}

    # Título e tamanho geral --------------------------------------------------------------------------------------------------------------

    if 'VACINA' in produto:
        titulo_colchetes = marca
    else:
        if cluster in ['BRONSTEIN', 'FRISCHMANN AISENGART', 'EXAME']:
            titulo_colchetes = marca
        else:
            titulo_colchetes = f"{marca} - {cluster}"

    fig.update_layout(height = positions['height'], width = 1500, title_text = f"[{titulo_colchetes}] {produto}",
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',)

    # Subítulos ---------------------------------------------------------------------------------------------------------------------------

    fig.update_layout(
        annotations=[
            dict(x = 0, y = positions['pos_y1'],
                xref ='paper', yref = 'paper',
                text = '<b>1. Volume x Preço - Pricing Points',
                showarrow = False,
                font = dict(size = 13)
            ),
            dict(x = 0, y = positions['pos_y2'],
                xref ='paper', yref = 'paper',
                text = '<b>2. Efeito da sazonalidade',
                showarrow = False,
                font = dict(size = 13)
            ),
            dict(x = 0, y = positions['pos_y3'],
                xref ='paper', yref = 'paper',
                text = '<b>3. Elasticidade',
                showarrow = False,
                font = dict(size = 13)
            ),
            dict(x = 0, y = positions['pos_y4'],
                xref ='paper', yref = 'paper',
                text = '<b>4. Performance histórica',
                showarrow = False,
                font = dict(size = 13)
            ),
            dict(x = 0, y = positions['pos_y5'],
                xref ='paper', yref = 'paper',
                text = '<b>5. Competitividade',
                showarrow = False,
                font = dict(size = 13)
            ),
        ]
    )

    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    # Salvar e mostrar gráfico
    # ----------------------------------------------------------------------------------------------------------------------------------------- #
    
    if show_fig:
        fig.show()
    
    if save_fig:
        if 'VACINA' in produto:
            path_grafico = os.path.join(path_entrega_final, 'Gráficos', 'One Page', f"{produto[:60].strip()}")
            os.makedirs(path_grafico, exist_ok = True)
            fig.write_html(os.path.join(path_grafico, f'{marca}.html'))
        else:
            if cluster in ['BRONSTEIN', 'FRISCHMANN AISENGART', 'EXAME']:
                path_grafico = os.path.join(path_entrega_final, 'Gráficos', 'One Page')
                os.makedirs(path_grafico, exist_ok = True)
                fig.write_html(os.path.join(path_grafico, f'{produto[:60].strip()}.html'))
            else:
                path_grafico = os.path.join(path_entrega_final, 'Gráficos', 'One Page', f"{produto[:60].strip()}")
                os.makedirs(path_grafico, exist_ok = True)
                fig.write_html(os.path.join(path_grafico, f'{cluster}.html'))
