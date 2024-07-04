from os import walk

pasta_dados = 'caminho_da_pasta'

files = []
for (dirpath, dirnames, filenames) in walk(pasta_dados):
    files.extend(filenames)
    break