import pandas as pd
import numpy as np
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

# ------------------------------------------------------------------------------------------------------- #
# Função para mostrar a distribuição das categorias das colunas
# ------------------------------------------------------------------------------------------------------- #

def categorias_colunas(df, n_max = 12):
    
    for coluna in df.columns:
        n_cat = df[coluna].nunique()
        n_missings = df[coluna].isna().sum()
        perc_missings = df[coluna].isna().mean()
        if n_cat <= n_max:
            print(f"Coluna: {coluna} | Qtd categorias: {n_cat} | Qtd missings: {n_missings} ({round(perc_missings * 100, 1)}%)")
            print(df[coluna].value_counts(dropna = False))
            print('-'*50)
            print()

    for coluna in df.columns:
        n_cat = df[coluna].nunique()
        n_missings = df[coluna].isna().sum()
        perc_missings = df[coluna].isna().mean()
        if n_cat > n_max:
            print(f"Coluna: {coluna} | Qtd categorias: {n_cat} | Qtd missings: {n_missings} ({round(perc_missings * 100, 1)}%)")
            print('-'*50)
            print()

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

# ----------------------------------------------------------------------------------------------------------------------- #
# Função para calcular o balanceamento da base 
# ----------------------------------------------------------------------------------------------------------------------- #

# dentro da coluna 1, qual é a proporção de cada categoria da coluna 2?

def calcular_balanceamento(df, coluna1, coluna2, metrica, print_series = False):

    # função entropia
    def entropy(proportions):
        return -np.sum(proportions * np.log2(proportions + 1e-10))  # Adiciona um pequeno valor para evitar log(0)
    
    # função índice de gini
    def gini_index(counts):
        total = sum(counts)
        sum_counts = sum([x * (total - x) for x in counts])
        return sum_counts / (total**2)
    
    if metrica not in ['gini', 'entropia']:
        return 'Métrica inválida'
    
    if metrica == 'gini':
        normalize = False
        metrica_title = 'Índice de Gini'
        nome_coluna = 'count'
        funcao = gini_index
    
    if metrica == 'entropia':
        normalize = True
        metrica_title = 'Entropia'
        nome_coluna = 'proportion'
        funcao = entropy
    
    class_counts = df.groupby(coluna1)[[coluna2]].value_counts(normalize = normalize).reset_index()

    for cat in df[coluna2].unique():
        series = class_counts[class_counts[coluna2] == cat][nome_coluna]
        result = funcao(series)
        print(cat)
        if print_series:
            print(series)
        print(f'{metrica_title}: {round(result, 4)}')
        print()

# ----------------------------------------------------------------------------------------------------------------------- #
# Função para printar o horário do término da execução
# ----------------------------------------------------------------------------------------------------------------------- #

def horario_atual(texto = "Término da execução"):
     from datetime import datetime
     import pytz

     hora_atual = datetime.now(pytz.timezone("America/Sao_Paulo"))
     print(f"{texto}: {hora_atual.strftime('%d/%m/%Y %H:%M:%S')}")

# ----------------------------------------------------------------------------------------------------------------------- #
# Função para printar um número com separador de milhar
# ----------------------------------------------------------------------------------------------------------------------- #

def sep_milhar(num, casas_decimais = 0):
    return f"{num:,.{casas_decimais}f}".replace(",", ".")