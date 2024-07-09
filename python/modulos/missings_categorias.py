import pandas as pd

def miss_cat_pd(df_) -> pd.DataFrame:
    ''' 
    Função que recebe um dataframe e retorna outro dataframe com o percentual de missings e o número de categorias de cada coluna 
    
    Args:
        df_: base de dados
    
    Returns: 
        pd.DataFrame: dataframe com 3 colunas: nome da coluna, percentual de missings da coluna e número de categorias da coluna 
    ''' 

    # lista vazia para anexar os percentuais de missings 
    perc_missings = [] 
    
    # lista das colunas do dataframe 
    colunas = df_.columns.tolist() 
    
    # calcula o número de missings de cada coluna 
    for coluna in colunas: 
        perc_miss = df_[coluna].isna().mean() * 100 
        perc_missings.append(perc_miss) 
    
    # lista vazia para anexar o número de categorias 
    n_categorias = [] 
    
    # calcular o número de categorias de cada coluna 
    for coluna in colunas: 
        n_cat = df_[coluna].nunique() 
        n_categorias.append(n_cat) 
 
    # junta tudo em um dataframe 
    df = pd.DataFrame(data = {'coluna': colunas,
                              'perc_missings': perc_missings,
                              'n_categorias': n_categorias}) 
    
    return df