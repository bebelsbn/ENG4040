# -------------------------------------------------------------------------------------------
# AVALIAÇÃO DO DESEMPENHO DO RANDOM FOREST POR SUBGRUPOS CLÍNICOS (CID-10)
#
# Este script aplica o modelo Random Forest separadamente para cada categoria CID-10
# presente na base clusterizada, com o objetivo de investigar o desempenho preditivo
# por subgrupos de doenças respiratórias.
#
# O foco está em comparar os valores de RMSE (erro quadrático médio) e R² para cada
# categoria, destacando a variação do desempenho do modelo ao lidar com diferentes
# perfis de doenças. Esse tipo de análise é fundamental para validar a hipótese de
# que segmentações mais específicas podem mitigar a dispersão observada nos modelos
# aplicados ao conjunto total de dados.
#
# A figura gerada  é utilizada na seção de Visualização dos Resultados e
# reforça as interpretações apresentadas na seção de Interpretação dos Resultados.
#
# Objetivo no trabalho:
# - Investigar a heterogeneidade da performance por doença
# - Avaliar se a clusterização por CID-10 gera ganhos de precisão
# - Apoiar decisões futuras sobre especialização de modelos
# -------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Caminho da base clusterizada
caminho = "Clustering/planilha/planilha_unificada_clusterizado.csv"

# Colunas
features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
target = "OBITOS"
coluna_cid = "Categoria CID-10"

# Carregamento
df = pd.read_csv(caminho)
df[target] = df[target].replace("-", np.nan)
for col in features + [target]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

resultados = []
for cid, grupo in df.groupby(coluna_cid):
    grupo = grupo[features + [target]].copy()
    grupo = grupo.fillna(grupo.median())

    scaler = StandardScaler()
    grupo[features] = scaler.fit_transform(grupo[features])

    X = grupo[features]
    y = grupo[target]

    if len(grupo) < 10 or y.nunique() <= 1:
        continue

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo = RandomForestRegressor(random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    # Pegar apenas o código (ex: J45)
    codigo_cid = cid.strip().split()[0]  

    resultados.append({
        "CID-10": codigo_cid,
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4),
        "N": len(grupo)
    })

df_resultados = pd.DataFrame(resultados).sort_values("RMSE")
print(df_resultados)


plt.figure(figsize=(10, 5))
sns.barplot(data=df_resultados, x="CID-10", y="RMSE", palette="crest")

plt.xticks(rotation=90, fontsize=10)
plt.title("Figura 24 – Comparação de RMSE dos modelos Random Forest por CID-10 (Clusterizado)", fontsize=12)
plt.xlabel("CID-10")
plt.ylabel("RMSE")
plt.tight_layout()
plt.savefig("figura24_rmse_clusterizado_melhorado.png")
plt.show()
