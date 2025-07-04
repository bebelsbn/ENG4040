import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings

warnings.filterwarnings("ignore")

# Caminhos dos arquivos
caminhos = {
    "Alta Sensibilidade": "Divisao/planilha_alta.csv",
    "Média Sensibilidade": "Divisao/planilha_media.csv",
    "Baixa Sensibilidade": "Divisao/planilha_baixa.csv",
    "Todas as Doenças (Clusterizado)": "Clustering/planilha/planilha_unificada_clusterizado.csv"
}

# Colunas numéricas e variável alvo
features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
target = "OBITOS"

# Função para avaliar o modelo
def avaliar_modelo(X, y, modelo):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    return rmse, r2

# Modelos a serem testados
modelos = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(random_state=42)
}

# Armazenar os resultados
resultados = []

# Loop pelos grupos
for grupo, caminho in caminhos.items():
    df = pd.read_csv(caminho)

    # Corrigir e converter colunas numéricas
    df[target] = df[target].replace("-", np.nan)
    for col in features + [target]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Criar base SEM pré-processamento
    df_sem_pre = df[features + [target]].dropna()

    # Criar base COM pré-processamento (imputação + normalização)
    df_com_pre = df[features + [target]].copy()
    for col in features + [target]:
        mediana = df_com_pre[col].median()
        df_com_pre[col] = df_com_pre[col].fillna(mediana)

    scaler = StandardScaler()
    df_com_pre[features] = scaler.fit_transform(df_com_pre[features])

    # Avaliar cada modelo
    for nome_modelo, modelo in modelos.items():
        # Avaliação SEM pré-processamento
        rmse_sem, r2_sem = avaliar_modelo(df_sem_pre[features], df_sem_pre[target], modelo)
        resultados.append({
            "Grupo": grupo,
            "Modelo": nome_modelo,
            "Pré-processamento": "Sem",
            "RMSE": round(rmse_sem, 4),
            "R2": round(r2_sem, 4)
        })

        # Avaliação COM pré-processamento
        rmse_com, r2_com = avaliar_modelo(df_com_pre[features], df_com_pre[target], modelo)
        resultados.append({
            "Grupo": grupo,
            "Modelo": nome_modelo,
            "Pré-processamento": "Com",
            "RMSE": round(rmse_com, 4),
            "R2": round(r2_com, 4)
        })

# Exibir resultados
df_resultados = pd.DataFrame(resultados)
print("\n📊 Comparação de Modelos (com vs sem pré-processamento):")
print(df_resultados)
