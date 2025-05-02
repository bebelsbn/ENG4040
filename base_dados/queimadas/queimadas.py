import pandas as pd
import glob

# Pasta onde estão os arquivos
queimadas_path = 'base_dados/queimadas'

# Lista para guardar os DataFrames
queimadas_list = []

# Ler e empilhar todos os arquivos queimadas_*.csv
for file in glob.glob(f'{queimadas_path}/queimadas_*.csv'):
    print(f"Lendo {file}")
    df = pd.read_csv(file)
    df['DataHora'] = pd.to_datetime(df['DataHora'], errors='coerce')
    df['Ano'] = df['DataHora'].dt.year
    df['Mes'] = df['DataHora'].dt.month
    queimadas_list.append(df)

# Concatenar tudo
queimadas_unificadas = pd.concat(queimadas_list, ignore_index=True)

# Reordenar colunas
colunas_finais = ['Ano', 'Mes', 'Satelite', 'Pais', 'Estado', 'Municipio', 'Bioma',
                  'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'Latitude', 'Longitude', 'FRP']

# Garantir que só essas colunas apareçam no final
queimadas_unificadas = queimadas_unificadas[colunas_finais]

# Exportar para CSV
queimadas_unificadas.to_csv('queimadas_unificadas.csv', index=False, encoding='utf-8')
print("✅ Arquivo 'queimadas_unificadas.csv' criado com sucesso!")
