import pandas as pd

# Substitua pelo caminho correto do seu arquivo CSV
file_path = "planilha_unificada.csv"
df = pd.read_csv(file_path, sep=";")

# Lista das colunas numéricas
cols_numericas = [
    "OBITOS", "AREA_DESMATADA_KM2", "FRP",
    "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"
]

# Garantir que são valores numéricos
df[cols_numericas] = df[cols_numericas].apply(pd.to_numeric, errors='coerce')

# Cálculo das estatísticas
estatisticas = df[cols_numericas].describe().T
estatisticas["variancia"] = df[cols_numericas].var()
estatisticas["mediana"] = df[cols_numericas].median()
estatisticas["missing"] = df[cols_numericas].isnull().sum()
estatisticas["missing_%"] = (estatisticas["missing"] / len(df)) * 100
estatisticas["count"] = df[cols_numericas].count()

# Reorganizar colunas
estatisticas = estatisticas[[
    "count", "missing", "missing_%", "mean", "std", "variancia", "min", "25%", "mediana", "50%", "75%", "max"
]]

# Exibir
print(estatisticas)
