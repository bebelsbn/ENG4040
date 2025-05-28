import pandas as pd
import os

# Caminho dos arquivos
folder = 'C:/Users/Allyson/ENG4040/base_dados/queimadas'
arquivos = [f for f in os.listdir(folder) if f.endswith('.csv')]

dfs = []

for arquivo in arquivos:
    path = os.path.join(folder, arquivo)
    df = pd.read_csv(path)

    df['DataHora'] = pd.to_datetime(df['DataHora'], errors='coerce')
    df['Ano'] = df['DataHora'].dt.year
    df['Mes'] = df['DataHora'].dt.month

    # Substitui valores de RiscoFogo -999 por NaN
    df['RiscoFogo'] = pd.to_numeric(df['RiscoFogo'], errors='coerce')
    df.loc[df['RiscoFogo'] <= -100, 'RiscoFogo'] = None  # valores inválidos

    dfs.append(df)

# Junta tudo
df_total = pd.concat(dfs)

# Agrupa por Ano, Mês e Satélite, calculando média
colunas_numericas = ['DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'Latitude', 'Longitude', 'FRP']
df_agrupado = df_total.groupby(['Ano', 'Mes', 'Satelite'])[colunas_numericas].mean().reset_index()

# Preenche meses ausentes
anos = sorted(df_total['Ano'].dropna().unique())
meses = range(1, 13)
satelites = df_total['Satelite'].dropna().unique()
index_completo = pd.MultiIndex.from_product([anos, meses, satelites], names=['Ano', 'Mes', 'Satelite'])
df_completo = pd.DataFrame(index=index_completo).reset_index()

# Junta com os dados reais
df_final = pd.merge(df_completo, df_agrupado, on=['Ano', 'Mes', 'Satelite'], how='left')
df_final.sort_values(by=['Ano', 'Mes', 'Satelite'], inplace=True)

# Salva
df_final.to_csv('queimadas_unificadas.csv', index=False)
print("Arquivo 'queimadas_unificadas.csv' criado com sucesso!")
