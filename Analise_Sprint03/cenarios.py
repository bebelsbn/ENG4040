import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings

warnings.filterwarnings("ignore")

# Caminho da base unificada clusterizada
caminho = "Clustering/planilha/planilha_unificada_clusterizado.csv"

# Features e target
features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
target = "OBITOS"
coluna_cid = "Categoria CID-10"

# Carregar base
df = pd.read_csv(caminho)

# Garantir dados numéricos
df[target] = df[target].replace("-", np.nan)
for col in features + [target]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Pré-processar por CID
resultados = []
for cid, grupo in df.groupby(coluna_cid):
    grupo = grupo[features + [target]].copy()
    for col in features + [target]:
        grupo[col] = grupo[col].fillna(grupo[col].median())
    
    # Escalar
    scaler = StandardScaler()
    grupo[features] = scaler.fit_transform(grupo[features])
    
    X = grupo[features]
    y = grupo[target]

    if len(grupo) < 10 or y.nunique() <= 1:
        continue  # Ignorar CID com poucos dados ou target constante

    # Treinar modelo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo = RandomForestRegressor(random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    
    # Métricas
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    resultados.append({
        "CID-10": cid,
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4),
        "N": len(grupo)
    })

# Mostrar resultados
df_resultados = pd.DataFrame(resultados).sort_values("RMSE")
print(df_resultados)


# ============================================================
# ANÁLISE DOS RESULTADOS POR CID-10 (Random Forest)
# 
# CID-10 com melhor desempenho (menor RMSE):
# - J45   Asma → RMSE = 0.5720, R² = -0.4721
# - J21   Bronquiolite aguda → RMSE = 0.7381
# - J81   Edema pulmonar NE → RMSE = 0.8150
#
# CID-10 com pior desempenho:
# - J12   Pneumonia viral NCOP → RMSE = 39.3303
# - J18   Pneumonia por micro-organismo NE → RMSE = 9.2870
# - J15   Pneumonia bacteriana NCOP → RMSE = 9.1928
#
# Interpretação:
# - O modelo teve melhor desempenho em doenças respiratórias **mais específicas** e com menor variabilidade nos dados.
# - CID-10 como **Asma (J45)**, **Bronquiolite (J21)** e **Edema Pulmonar (J81)** apresentaram RMSE muito baixos, indicando previsões mais precisas.
# - Por outro lado, doenças como **Pneumonias (J12, J15, J18)** apresentaram grande erro, possivelmente por maior heterogeneidade dos casos.
#
# Observação:
# - Alguns CIDs possuem poucos registros (N < 20), o que pode prejudicar a generalização do modelo.
# - O valor de R² negativo indica que o modelo previu pior do que a média dos dados em vários casos.
# ============================================================
