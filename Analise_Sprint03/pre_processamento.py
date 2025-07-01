import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error

# Carregar os dados
df = pd.read_csv("Divisao/planilha_alta.csv", sep=",")  # separador corrigido

# Selecionar colunas relevantes
features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
target = "OBITOS"

# Limpeza
df[features + [target]] = df[features + [target]].replace("-", np.nan)
df[features + [target]] = df[features + [target]].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=features + [target])

# Separar variáveis preditoras e alvo
X = df[features]
y = df[target]

# Separar em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

def avaliar_modelo(nome, modelo, X_tr, X_ts, y_tr, y_ts):
    modelo.fit(X_tr, y_tr)
    y_pred = modelo.predict(X_ts)
    r2 = r2_score(y_ts, y_pred)
    rmse = np.sqrt(mean_squared_error(y_ts, y_pred))
    print(f"🔹 {nome}: R² = {r2:.3f} | RMSE = {rmse:.2f}")

print("📊 AVALIAÇÃO DE MODELOS SEM PRÉ-PROCESSAMENTO")
avaliar_modelo("Regressão Linear", LinearRegression(), X_train, X_test, y_train, y_test)
avaliar_modelo("Random Forest", RandomForestRegressor(random_state=42), X_train, X_test, y_train, y_test)

# Aplicar pré-processamento (normalização)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("\n📊 AVALIAÇÃO DE MODELOS COM PRÉ-PROCESSAMENTO")
avaliar_modelo("Regressão Linear", LinearRegression(), X_train_scaled, X_test_scaled, y_train, y_test)
avaliar_modelo("Random Forest", RandomForestRegressor(random_state=42), X_train_scaled, X_test_scaled, y_train, y_test)
