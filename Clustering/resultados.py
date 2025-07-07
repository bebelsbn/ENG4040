import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Carregar base unificada com todas as doenças (inclui PM2.5 e FRP)
df = pd.read_csv("Clustering/planilha/planilha_unificada_clusterizado.csv")

# Converter e tratar colunas
df['OBITOS'] = pd.to_numeric(df['OBITOS'], errors='coerce')
df['FRP'] = pd.to_numeric(df['FRP'], errors='coerce')
df['pm2.5_atm'] = pd.to_numeric(df['pm2.5_atm'], errors='coerce')

df = df[['FRP', 'pm2.5_atm', 'OBITOS']].dropna()

# Escalar as variáveis
scaler = StandardScaler()
X = scaler.fit_transform(df[['FRP', 'pm2.5_atm']])
y = df['OBITOS'].values

# Regressão Linear Simples com FRP e PM2.5
modelo = LinearRegression()
modelo.fit(X, y)
y_pred = modelo.predict(X)
r2 = r2_score(y, y_pred)

# Exibir os coeficientes
print("📊 Coeficientes da Regressão Linear:")
print(f"FRP        → coef = {modelo.coef_[0]:.4f}")
print(f"PM2.5_atm  → coef = {modelo.coef_[1]:.4f}")
print(f"Intercepto → {modelo.intercept_:.4f}")
print(f"R² do modelo: {r2:.4f}")

# Gráficos de dispersão
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.regplot(data=df, x='FRP', y='OBITOS', scatter_kws={'alpha':0.5})
plt.title("Relação entre FRP e Óbitos")

plt.subplot(1, 2, 2)
sns.regplot(data=df, x='pm2.5_atm', y='OBITOS', scatter_kws={'alpha':0.5}, color='orange')
plt.title("Relação entre PM2.5 e Óbitos")

plt.tight_layout()
plt.show()
