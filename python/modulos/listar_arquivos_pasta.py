from os import walk
from typing import List

def listar_arquivos_pasta(folder_path: str) -> List[str]:

    files = []
    for (dirpath, dirnames, filenames) in walk(folder_path):
        files.extend(filenames)
        break

    return files