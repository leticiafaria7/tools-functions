import pandas as pd
import numpy as np

def base_quantis_agrupados(df, coluna_valores, init = 0.1, inc = 0.05):
    tmp = df.copy()

    values = {}
    init = init
    inc = inc
    
    for q in [init] + list(np.arrange(init + inc, 1.01, inc)):
        v = np.quantile(tmp([coluna_valores], min(q, 1)))
        values[v] = q

    def get_quantile(preco, values = values):
        for (k, v) in values.items():
            if preco <= k:
                return v
            
    def get_price(preco, values = values):
        for (k, v) in values.items():
            if preco <= k:
                return k
    
    tmp['quantile'] = tmp[coluna_valores].apply(get_quantile)
    tmp['price'] = tmp[coluna_valores].apply(get_price)

    tmp = tmp.groupby('price').size().reset_index(name = 'qtd')

    return tmp
