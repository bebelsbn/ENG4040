import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Limiar da OMS para PM2.5 (μg/m³)
PM25_LIMIAR = 25.0

# Carregar dados com separador correto
df = pd.read_csv("Divisao/planilha_alta.csv", sep=",", encoding="utf-8", engine="python")

# Confirmar as colunas
print("✅ Colunas reais:", df.columns.tolist())

# Padronizar nomes de colunas (remover espaços e deixar em minúsculo)
df.columns = df.columns.str.strip().str.lower()

# Verificar se as colunas essenciais existem
if "obitos" not in df.columns or "pm2.5_atm" not in df.columns:
    print("❌ As colunas 'obitos' ou 'pm2.5_atm' não foram encontradas.")
    exit()

# Substituir "-" por NaN e converter colunas numéricas
df[["obitos", "pm2.5_atm"]] = df[["obitos", "pm2.5_atm"]].replace("-", np.nan)
df[["obitos", "pm2.5_atm"]] = df[["obitos", "pm2.5_atm"]].apply(pd.to_numeric, errors="coerce")

# Remover linhas inválidas
df = df.dropna(subset=["obitos", "pm2.5_atm"])

# Criar coluna de exposição alta
df["exposicao_alta"] = (df["pm2.5_atm"] > PM25_LIMIAR).astype(int)

# Separar os grupos
grupo_baixa = df[df["exposicao_alta"] == 0]["obitos"]
grupo_alta  = df[df["exposicao_alta"] == 1]["obitos"]

# Estatísticas descritivas
print("\n🔍 Média de óbitos por grupo de exposição:")
print(f"➡️ Exposição BAIXA: {grupo_baixa.mean():.2f} óbitos")
print(f"➡️ Exposição ALTA:  {grupo_alta.mean():.2f} óbitos")

# Teste t de diferença de médias
t_stat, p_val = ttest_ind(grupo_baixa, grupo_alta, equal_var=False)
print(f"\n📊 Teste t: t = {t_stat:.2f}, p = {p_val:.4f}")

# Visualização
plt.figure(figsize=(8, 5))
sns.boxplot(x="exposicao_alta", y="obitos", data=df)
plt.xticks([0, 1], ["Baixa exposição", "Alta exposição"])
plt.title("Óbitos por Doenças Respiratórias vs. Exposição a PM2.5")
plt.ylabel("Número de Óbitos")
plt.xlabel("Exposição a PM2.5 (>25 µg/m³)")
plt.tight_layout()
plt.show()
