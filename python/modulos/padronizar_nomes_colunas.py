import unicodedata
import pandas as pd

def remove_acentos(texto):
	return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
	
def padronizar_nomes_colunas(df_):
	
    nomes_padronizados = []
	
    for coluna in df_.columns:
        coluna = coluna.lower()
        coluna = remove_acentos(coluna)
        coluna = coluna.replace(' ', '_')
        nomes_padronizados.append(coluna)
		
    return nomes_padronizados

# ------------------------------------------------------------------------------ #
# exemplo
# ------------------------------------------------------------------------------ #

"""
df = pd.DataFrame()
df.columns = padronizar_nomes_colunas(df)

"""
