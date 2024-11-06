import numpy as np

def calcular_balanceamento(df, coluna1, coluna2, metrica, print_series = False):

    # função entropia
    def entropy(proportions):
        return -np.sum(proportions * np.log2(proportions + 1e-10))  # adicionar um pequeno valor para evitar log(0)
    
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