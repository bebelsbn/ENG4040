import os
import pandas as pd

# Caminho para a pasta com os CSVs
pasta_csvs = "base_dados/qualidade_Ar"

# Lista para armazenar os DataFrames de cada sensor
dataframes = []

# Percorrer todos os arquivos CSV da pasta
for nome_arquivo in os.listdir(pasta_csvs):
    if nome_arquivo.endswith(".csv"):
        caminho = os.path.join(pasta_csvs, nome_arquivo)
        df = pd.read_csv(caminho)

        # Converte timestamp ISO para datetime
        df['datetime'] = pd.to_datetime(df['time_stamp'], utc=True)
        df['ano'] = df['datetime'].dt.year
        df['mes'] = df['datetime'].dt.month

        # Agrupa por ano e mês e calcula a média dos campos desejados
        df_media = df.groupby(['ano', 'mes'])[['pm2.5_atm', 'humidity', 'temperature', 'pressure']].mean().reset_index()
        dataframes.append(df_media)

# Unifica todos os sensores pela média entre eles
df_unificado = pd.concat(dataframes).groupby(['ano', 'mes']).mean().reset_index()

# Exibe o resultado final
print(df_unificado)

# (Opcional) salva em CSV
df_unificado.to_csv("media_mensal_qualidade_ar_manaus.csv", sep=';', index=False)
