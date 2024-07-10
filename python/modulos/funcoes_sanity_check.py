import pandas as pd
import textdistance as td

# ----------------------------------------------------------------------------------------------------------------------- #
# Verificar o percentual de missings e número de categorias de cada coluna
# ----------------------------------------------------------------------------------------------------------------------- #

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

# ----------------------------------------------------------------------------------------------------------------------- #
# Contar e calcular o percentual de cada categoria de uma coluna
# ----------------------------------------------------------------------------------------------------------------------- #

def cont_perc_categorias(df_, coluna):
    df_temp = df_.copy()
    df_temp = df_temp[coluna].value_counts(dropna = False).reset_index()
    df_temp['perc'] = round(df_temp['count'] * 100 / df_temp['count'].sum(), 3)

    return df_temp

# ----------------------------------------------------------------------------------------------------------------------- #
# Função para encontrar pares de palavras similares (jaro-winkler)
# ----------------------------------------------------------------------------------------------------------------------- #

def find_similar_pairs(texts: pd.Series, threshold = 0.75):

    """
    Função que encontra pares de palavras similares em uma coluna.

    Args:
        - texts (pd.Series): coluna do dataframe
        - threshold (float): corte de similaridade, entre 0 e 1. Quando mais próximo de 1, maior deve ser a similaridade.
                             Para colunas com muitas categorias e muitos nomes parecidos, se o threshold for muito baixo, 
                             pode demorar bastante para executar a função
    
    Returns:
        - pd.DataFrame: dataframe com 3 colunas: componente 1 do par, componente 2 do par e número de ocorrências

    Exemplo de uso:

    tmp = find_similar_pairs(df[['coluna']].drop_duplicates()['coluna'], 0.95)
    with pd.option_context('display.max_rows', None):
        display(tmp)
    
    """
    texts = texts.astype(str)
    count_texts = texts.value_counts(dropna=False).to_dict()
    unique_texts = texts.unique()
    similar_pairs = []

    for i in range(len(unique_texts)):
        for j in range(i+1, len(unique_texts)):
            text_1 = unique_texts[i]
            text_2 = unique_texts[j]
            similarity = td.jaro(text_1, text_2)

            if similarity > threshold:
                similar_pairs.append((text_1, text_2, similarity))
            
    df_similar_pairs = pd.DataFrame(similar_pairs, columns=['text', 'similar_text', 'similarity'])
    
    if df_similar_pairs.empty:
        return df_similar_pairs
    
    df_similar_pairs[['text', 'similar_text']] = df_similar_pairs\
        .apply(lambda row: tuple(sorted([row['text'], row['similar_text']], 
                                        key = lambda x: count_texts[x], 
                                        reverse = True)), axis = 1).apply(pd.Series)
    
    return df_similar_pairs.sort_values(['similarity'], ascending=False).reset_index(drop=True)