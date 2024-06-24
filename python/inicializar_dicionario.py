
# inicializar um dicionário que terá um dicionário para cada chave

# sub dicionários
def init_sub_dict(default_values: dict):
    d = {}
    for key, value in default_values.items():
        d[key] = value
    return d

# dicionário geral
def init_dict(keys, dv):
    d = {}
    for key in keys:
        d[key] = init_sub_dict(dv)
    return d

# exemplo
default_dict = {
    'chave1':[],
    'chave2': '',
    'chave3': False
}

marcas = ['marca1', 'marca2', 'marca']

dict_marcasw = init_dict(marcas, default_dict)