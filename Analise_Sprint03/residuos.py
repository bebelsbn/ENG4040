# -------------------------------------------------------------------------------------------
# ANÁLISE DOS RESÍDUOS DO MODELO RANDOM FOREST - ALTA SENSIBILIDADE
#
# Objetivo:
# Avaliar a qualidade dos ajustes do modelo Random Forest para o grupo de doenças
# respiratórias de Alta Sensibilidade por meio da análise dos resíduos (erros de previsão).
#
# Importância no trabalho:
# A análise dos resíduos é essencial para verificar a presença de padrões não capturados 
# pelo modelo, viés sistemático e possíveis limitações no desempenho preditivo. 
# Ajuda a identificar se o modelo está superestimando ou subestimando óbitos em certos cenários.
#
# Etapas realizadas:
# - Leitura da base de dados da categoria Alta Sensibilidade
# - Imputação de valores ausentes com KNN (k=5)
# - Remoção de colunas altamente correlacionadas (acima de 0.9)
# - Normalização robusta com PowerTransformer (transformação não linear)
# - Treinamento do modelo Random Forest
# - Geração de gráficos para análise dos resíduos:
#     * Boxplot para verificar simetria e outliers
#     * Dispersão dos resíduos vs valores preditos para avaliar viés
# - Cálculo das métricas RMSE e R² para quantificar o desempenho
# -------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error, r2_score

# === Carrega a planilha ===
df = pd.read_csv("Divisao/planilha_alta.csv")

# === Define colunas relevantes ===
features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
target = "OBITOS"

# === Converte "-" em NaN e para valores numéricos ===
for col in features + [target]:
    df[col] = pd.to_numeric(df[col].replace("-", np.nan), errors="coerce")

# === Remove linhas sem target ===
df.dropna(subset=[target], inplace=True)

# === Imputação com KNN ===
imputer = KNNImputer(n_neighbors=5)
df[features] = imputer.fit_transform(df[features])

# === Remoção de features com alta correlação ===
corr = df[features].corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
features_corr_ok = [col for col in features if all(upper[col] < 0.9)]

# Se removeu todas, usa os originais
if not features_corr_ok:
    print("⚠️ Nenhuma variável sobrou após verificação de correlação. Usando todas.")
    features_corr_ok = features

df = df[features_corr_ok + [target]]

# === Normalização robusta ===
scaler = PowerTransformer()
df[features_corr_ok] = scaler.fit_transform(df[features_corr_ok])

# === Treinamento ===
X = df[features_corr_ok]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

modelo = RandomForestRegressor(random_state=42)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

# === Cálculo dos resíduos ===
residuos = y_test - y_pred

# === Gráfico 1: Boxplot dos resíduos ===
plt.figure(figsize=(6, 5))
sns.boxplot(y=residuos)
plt.title("Boxplot dos Resíduos (Random Forest - Alta)")
plt.ylabel("Resíduos")
plt.tight_layout()
plt.savefig("boxplot_residuos_alta.png")
plt.show()

# === Gráfico 2: Dispersão dos resíduos ===
plt.figure(figsize=(7, 5))
sns.scatterplot(x=y_pred, y=residuos)
plt.axhline(0, color='red', linestyle='--')
plt.title("Dispersão dos Resíduos vs. Valores Preditos")
plt.xlabel("Valores Preditos")
plt.ylabel("Resíduos")
plt.tight_layout()
plt.savefig("dispersao_residuos_alta.png")
plt.show()

# === Métricas ===
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f"\n📊 RMSE = {rmse:.4f} | R² = {r2:.4f}")
