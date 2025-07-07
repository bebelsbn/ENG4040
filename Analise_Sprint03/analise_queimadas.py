# -------------------------------------------------------------------------------------------
# AVALIAÇÃO DE MODELOS PREDITIVOS E RELAÇÕES ENTRE VARIÁVEIS AMBIENTAIS E ÓBITOS
#
# Este script realiza a comparação entre dois modelos de regressão (Linear e Random Forest)
# para prever o número de óbitos por doenças respiratórias a partir de variáveis ambientais,
# considerando diferentes agrupamentos por sensibilidade (Alta, Média, Baixa e Todas as Doenças).
#
# Além disso, calcula correlações entre óbitos e variáveis como PM2.5, FRP e dias sem chuva,
# e gera visualizações para facilitar a interpretação dos resultados.
#
# Objetivo no trabalho:
# - Avaliar o desempenho dos modelos em diferentes grupos de sensibilidade
# - Identificar variáveis ambientais mais correlacionadas com óbitos
# - Explorar padrões por meio de scatter plots, linha de tendência e heatmaps
#
# Essa análise compõe parte da seção de Visualização dos Resultados e Interpretação do relatório,
# reforçando as descobertas estatísticas com gráficos e comparações objetivas entre modelos.
# -------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

import warnings
warnings.filterwarnings("ignore")

# Caminhos dos dados
caminhos = {
    "Alta Sensibilidade": "Divisao/planilha_alta.csv",
    "Média Sensibilidade": "Divisao/planilha_media.csv",
    "Baixa Sensibilidade": "Divisao/planilha_baixa.csv",
    "Todas as Doenças": "Clustering/planilha/planilha_unificada_clusterizado.csv"
}

features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
target = "OBITOS"

# Avaliação e coleta de resultados
resultados = []

for grupo, caminho in caminhos.items():
    df = pd.read_csv(caminho)

    # Preparo
    df[target] = df[target].replace("-", np.nan)
    for col in features + [target]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[features + [target]].dropna()
    for col in df.columns:
        df[col] = df[col].fillna(df[col].median())
    df[features] = StandardScaler().fit_transform(df[features])

    X = df[features]
    y = df[target]

    # Modelos
    lr = LinearRegression()
    rf = RandomForestRegressor(random_state=42)

    # Treino/teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    lr.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    y_pred_lr = lr.predict(X_test)
    y_pred_rf = rf.predict(X_test)

    # Métricas
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    r2_lr = r2_score(y_test, y_pred_lr)

    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    r2_rf = r2_score(y_test, y_pred_rf)

    resultados.append({
        "Grupo": grupo,
        "Modelo": "Linear Regression",
        "RMSE": round(rmse_lr, 4),
        "R2": round(r2_lr, 4)
    })

    resultados.append({
        "Grupo": grupo,
        "Modelo": "Random Forest",
        "RMSE": round(rmse_rf, 4),
        "R2": round(r2_rf, 4)
    })

# Resultado final
df_resultados = pd.DataFrame(resultados)
print("\n📊 Comparação de Desempenho:")
print(df_resultados)

# Correlação com variáveis ambientais (exemplo Todas as Doenças)
df_todas = pd.read_csv("Clustering/planilha/planilha_unificada_clusterizado.csv")
df_todas[target] = pd.to_numeric(df_todas[target], errors="coerce")
corr = df_todas[["OBITOS", "FRP", "DIASEMCHUVA", "pm2.5_atm"]].corr()["OBITOS"].drop("OBITOS")
print("\n📈 Correlação com variáveis ambientais:")
print(corr)

# Visualização (opcional)
sns.pairplot(df_todas[["OBITOS", "FRP", "DIASEMCHUVA", "pm2.5_atm"]])
plt.suptitle("Relação entre Óbitos e variáveis ambientais", y=1.02)
plt.tight_layout()
plt.show()


def scatter_with_trend(x, y, xlabel, ylabel, title):
    plt.figure(figsize=(8,5))
    sns.regplot(x=x, y=y, data=df, scatter_kws={"s": 30}, line_kws={"color": "red"})
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.show()

# Correlação OBITOS vs FRP
scatter_with_trend('FRP', 'OBITOS', 'FRP (Focos de Queimada)', 'Óbitos', 'Correlação entre FRP e Óbitos')

# Correlação OBITOS vs PM2.5
scatter_with_trend('PM2.5_atm', 'OBITOS', 'PM2.5 Atmosférico', 'Óbitos', 'Correlação entre PM2.5 e Óbitos')

# Correlação OBITOS vs Dias sem chuva
scatter_with_trend('DIASEMCHUVA', 'OBITOS', 'Dias sem chuva', 'Óbitos', 'Correlação entre Seca e Óbitos')

# Heatmap da matriz de correlação
plt.figure(figsize=(6,5))
corr = df[['OBITOS', 'FRP', 'PM2.5_atm', 'DIASEMCHUVA']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Matriz de Correlação entre Variáveis")
plt.show()