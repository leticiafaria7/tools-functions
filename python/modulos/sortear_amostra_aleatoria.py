import random
import numpy as np

def sortear_amostra_aleatoria(min, max, n, seed = None, repetir = False):

    if seed is not None:
        np.random.seed(seed) if repetir else random.seed(seed)

    if repetir:
        amostra_aleatoria = np.random.randint(low = min, high = max + 1, size = n).tolist()
        amostra_aleatoria = sorted(amostra_aleatoria)
    else:
        amostra_aleatoria = random.sample(range(min, max + 1), n)
        amostra_aleatoria = sorted(amostra_aleatoria)

    return amostra_aleatoria
