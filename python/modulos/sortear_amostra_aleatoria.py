import random
import numpy as np

def sortear_amostra_aleatoria(min, max, n, seed = 101, repetir = False):

    if repetir:
        np.random.seed(seed)
        amostra_aleatoria = np.random.randint(low = min, high = max + 1, size = n).tolist()
        amostra_aleatoria = sorted(amostra_aleatoria)
    else:
        random.seed(101)
        amostra_aleatoria = random.sample(range(min, max + 1), n)
        amostra_aleatoria = sorted(amostra_aleatoria)

    return amostra_aleatoria