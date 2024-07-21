# pega a url da paleta gerada e transforma em uma lista com o # no início de cada cor

def transform_list_coolors(str):
    str = '#' + str
    list = str.replace('-', '-#').split('-')
    return list