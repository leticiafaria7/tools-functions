import numpy as np
from scipy.stats import skew

def calcular_assimetria_distribuicao(dados: np.array, titulo):

    dados = np.array(dados)

    # Calcula Q1 (25º percentil) e Q3 (75º percentil)
    Q1 = np.percentile(dados, 25)
    Q2 = np.percentile(dados, 50)
    Q3 = np.percentile(dados, 75)

    # Calcula o IQR
    IQR = Q3 - Q1

    # Calcula o coeficiente de assimetria (skewness)
    skewness = skew(dados)

    # Ajusta os multiplicadores com base na skewness
    if skewness > 0:
        k_inferior = 1.5
        k_superior = 1.5 + skewness # Aumenta o multiplicador superior
    elif skewness < 0:
        k_inferior = 1.5 + abs(skewness) # Aumenta o multiplicador inferior
        k_superior = 1.5
    else:
        k_inferior = 1.5
        k_superior = 1.5

    # Calcula os limites para outliers
    limite_inferior = Q1 - k_inferior * IQR
    limite_superior = Q3 + k_superior * IQR

    # Identifica os outliers
    outliers = dados[(dados < limite_inferior) | (dados > limite_superior)]

    print(f"Box-plot - {titulo}")
    print('-' * 40)

    print("Q1:", Q1)
    print("Q2:", Q2)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("Skewness:", skewness)
    print("Limite Inferior:", limite_inferior)
    print("Limite Superior:", limite_superior)
    print("Outliers:", outliers)
