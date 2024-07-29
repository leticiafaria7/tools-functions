import unicodedata

def remove_acentos(texto):
	return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))