import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression, RFE
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

# === Funções auxiliares ===
def identificar_estacao(mes):
    if mes in [12, 1, 2]: return 'verao'
    elif mes in [3, 4, 5]: return 'outono'
    elif mes in [6, 7, 8]: return 'inverno'
    else: return 'primavera'

mapa_qualidade = {"Boa": 0, "Moderada": 1, "Ruim": 2, "Muito Ruim": 3, "Péssima": 4}

def avaliar_metricas(y_true, y_pred, X_test):
    n = len(y_true)
    p = X_test.shape[1]
    r2 = r2_score(y_true, y_pred)
    r2_ajustado = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {"RMSE": rmse, "R2": r2, "R2_Ajustado": r2_ajustado}

# === Carregamento ===
df = pd.read_csv("/Users/mariaisabel/Documents/PUC/5°Periodo/Projeto CD/ENG4040/Divisao/planilha_media.csv")

# === Preprocessamento ===
numericas = ["OBITOS", "AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
df[numericas] = df[numericas].apply(pd.to_numeric, errors="coerce")
df["estacao"] = df["mes"].apply(identificar_estacao)
df["qualidade_ar_ordinal"] = df["QUALIDADE_AR_CLASSIFICADA"].map(mapa_qualidade)
df["log_OBITOS"] = np.log1p(df["OBITOS"])
df = pd.get_dummies(df, columns=["Categoria CID-10", "estacao"], drop_first=True)

# === Features ===
features_base = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm", "qualidade_ar_ordinal"]
features_base += [col for col in df.columns if col.startswith("Categoria CID-10_") or col.startswith("estacao_")]

X = df[features_base].fillna(df[features_base].mean())
y = df["log_OBITOS"].fillna(df["log_OBITOS"].mean())

# === Split 70/30 ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# === Modelos e Seletores ===
modelos = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(random_state=42)
}
seletores = {
    "SelectKBest": SelectKBest(score_func=f_regression, k=10),
    "RFE": RFE(estimator=LinearRegression(), n_features_to_select=10)
}

# === Execução com Cross-Validation ===
resultados = []

for nome_sel, seletor in seletores.items():
    seletor.fit(X_train, y_train)
    X_train_sel = seletor.transform(X_train)
    X_test_sel = seletor.transform(X_test)

    for nome_mod, modelo in modelos.items():
        modelo.fit(X_train_sel, y_train)
        y_pred_test = modelo.predict(X_test_sel)

        # Treino com cross-val
        kf = KFold(n_splits=3, shuffle=True, random_state=42)
        y_pred_train_cv = cross_val_predict(modelo, X_train_sel, y_train, cv=kf)

        metricas_treino = avaliar_metricas(y_train, y_pred_train_cv, X_train_sel)
        metricas_teste = avaliar_metricas(y_test, y_pred_test, X_test_sel)

        resultados.append({
            "Modelo": nome_mod,
            "Seletor": nome_sel,
            "RMSE_Treino": round(metricas_treino["RMSE"], 4),
            "RMSE_Teste": round(metricas_teste["RMSE"], 4),
            "R2_Treino": round(metricas_treino["R2"], 4),
            "R2_Teste": round(metricas_teste["R2"], 4),
            "R2_Ajustado_Treino": round(metricas_treino["R2_Ajustado"], 4),
            "R2_Ajustado_Teste": round(metricas_teste["R2_Ajustado"], 4),
        })

# === Exportar para Excel ===
import os
output_dir = "/Users/mariaisabel/Documents/PUC/5°Periodo/Projeto CD/ENG4040/PlanoEx/Excel"
os.makedirs(output_dir, exist_ok=True)

# Criar o DataFrame com os resultados
df_resultados = pd.DataFrame(resultados)

# Caminho para salvar o Excel
caminho_excel = os.path.join(output_dir, "plano_experimentacao_resultados_alta.xlsx")

# Exportar para Excel
df_resultados.to_excel(caminho_excel, index=False)

print(f"Arquivo Excel salvo em: {caminho_excel}")

print("✅ Arquivo salvo como 'plano_experimentacao_resultados.xlsx'")
