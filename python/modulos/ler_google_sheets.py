import pandas as pd

def ler_google_sheets(sheet_id, sheet_name):
    url_df = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    df = pd.read_csv(url_df)
    return df

ler_google_sheets(sheet_id = '1lzq0k-41-MbbS63C3Q9i1wPvLkSJt9zhr4Jolt1vEog',
                  sheet_name = 'emissoes_percapita')