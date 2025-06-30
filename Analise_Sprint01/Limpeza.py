import pandas as pd

# === Carregar planilha unificada ===
file_path = 'planilha_unificada.csv'  # ajuste para seu arquivo
df = pd.read_csv(file_path)

# Padronizar nomes de município
df['municipality'] = df['municipality'].str.strip().str.upper()

# Forçar conversão das colunas numéricas
numeric_columns = ['year', 'month', 'deaths', 'DiaSemChuva',
                   'Precipitacao', 'RiscoFogo', 'FRP', 'area_desmatada_km2']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Exportar DataFrame final mantendo os NaN
output_file = 'planilha_unificada_final_nan.csv'
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"✅ Base final salva (mantendo NaN) em: {output_file}")
