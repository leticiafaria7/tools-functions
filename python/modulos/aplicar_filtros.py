# função
def aplicar_filtros(df, dict_filtro):
    for (k, v) in dict_filtro.items:
        df_filtered = df_filtered[df_filtered[k].isin(v)].copy()

    return df_filtered
  
# exemplo de aplicação
# dict_filtro = {'coluna_1':['cat_1', 'cat_2'],
#                'coluna_2':['cat_3']}