import pandas as pd

# Caminho do arquivo CSV
caminho_arquivo = "planilha_unificada.csv"  # substitua pelo nome real

# Lê o CSV
df = pd.read_csv(caminho_arquivo, sep=";")  # ajuste o separador se necessário

# Exibe quantidade de linhas e colunas
print(f"Número de linhas: {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")

# Exibe os nomes das colunas
print("Colunas:")
print(df.columns.tolist())

import pandas as pd

# Conta valores nulos por coluna
nulos_por_coluna = df.isnull().sum()

# Exibe o resultado
print("\nValores nulos por coluna:")
print(nulos_por_coluna)
