import pandas as pd

# Carregar a base de dados
df = pd.read_csv('planilha_unificada.csv')

# Selecionar as colunas de interesse
cols = ['deaths', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'FRP', 'area_desmatada_km2']
municipio_col = 'municipality'

# Garantir que todas as colunas sejam numéricas
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ---------- Estatísticas gerais (dados originais) ----------
desc_original = df[cols].describe()
print("\n--- Estatísticas gerais (dados originais) ---")
print(desc_original)

# ---------- Contagem de nulos por município ----------
null_counts = df.groupby(municipio_col)[cols].apply(lambda x: x.isnull().sum())
total_counts = df.groupby(municipio_col)[cols].count() + null_counts
null_proportion = null_counts / (null_counts + total_counts)

print("\n--- Proporção de nulos por município ---")
print(null_proportion)

# ---------- Preencher nulos pela média do município ----------
df_filled = df.copy()
for col in cols:
    df_filled[col] = df.groupby(municipio_col)[col].transform(lambda x: x.fillna(x.mean()))

desc_filled = df_filled[cols].describe()
print("\n--- Estatísticas com nulos preenchidos pela média ---")
print(desc_filled)
