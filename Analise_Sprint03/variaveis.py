import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

def analisar_variaveis(df, nome_tabela):
    print(f"\n🔍 ANÁLISE DE VARIÁVEIS - {nome_tabela}")

    features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
    target = "OBITOS"
    
    X = df[features]

    
    X = X.fillna(X.mean())
    y = pd.to_numeric(df[target], errors="coerce")  # força conversão para numérico, vira NaN se inválido
    y = y.fillna(y.mean())  # preenche os NaNs resultantes


    # Separar em treino e teste (para consistência, mesmo que não use test)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)

    # Regressão Linear: Coeficientes
    modelo_lr = LinearRegression()
    modelo_lr.fit(X_train, y_train)
    coef_lr = modelo_lr.coef_

    print("\nCoeficientes da Regressão Linear:")
    for var, coef in zip(features, coef_lr):
        print(f"{var:20}: {coef:.4f}")

    # Random Forest: Importância das variáveis
    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)
    importancias_rf = modelo_rf.feature_importances_

    print("\nImportância das Variáveis (Random Forest):")
    for var, imp in sorted(zip(features, importancias_rf), key=lambda x: x[1], reverse=True):
        print(f"{var:20}: {imp:.4f}")

# Ler as tabelas
tabelas = {
    "Alta Sensibilidade": pd.read_csv("Divisao/planilha_alta.csv"),
    "Média Sensibilidade": pd.read_csv("Divisao/planilha_media.csv"),
    "Baixa Sensibilidade": pd.read_csv("Divisao/planilha_baixa.csv"),
    "Unficada": pd.read_csv("planilha_unificada.csv",sep=";")
}

# Analisar variáveis
for nome, df in tabelas.items():
    analisar_variaveis(df, nome)
