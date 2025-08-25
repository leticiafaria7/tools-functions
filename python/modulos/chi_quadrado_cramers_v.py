
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

def cramers_v(df, var1, var2, relatorio = True):

    observado = pd.crosstab(df[var1], df[var2])
    chi2, p, dof, expected = chi2_contingency(observado)
    esperado = pd.DataFrame(expected, index = observado.index, columns = observado.columns)
    n = observado.sum().sum()
    r, k = observado.shape
    v = (chi2 / n)**0.5 / min(k - 1, r - 1)

    if relatorio:
        print(f"Qui-quadrado: {chi2:.4f}")
        print(f"P-valor: {p:.4f}")
        print(f"Cramér's V: {v:.4f}")
        print()
        print(f"***Interpretação da medida de associação Cramér's V:***")
        print(f"0.00 a 0.10 | Muito fraca ou nenhuma associação")
        print(f"0.10 a 0.20 | Fraca")
        print(f"0.20 a 0.40 | Moderada")
        print(f"0.40 a 0.60 | Forte")
        print(f"0.60 a 1.00 | Muito forte")
        print()

        delta = (observado - esperado)
        plt.figure(figsize = (16, 5))
        ax = sns.heatmap(delta, cmap = 'RdBu', annot = True, fmt = '.0f')
        ax = ax

    return chi2, p, v
