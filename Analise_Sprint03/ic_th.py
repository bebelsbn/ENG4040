import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from scipy.stats import ttest_rel
import warnings
warnings.filterwarnings("ignore")

# === Configurações ===
N_ITER = 1000  # Nº de iterações de bootstrap
TEST_SIZE = 0.3
RANDOM_STATE = 42

# === Caminhos ===
caminhos = {
    "Alta Sensibilidade": "Divisao/planilha_alta.csv",
    "Média Sensibilidade": "Divisao/planilha_media.csv",
    "Baixa Sensibilidade": "Divisao/planilha_baixa.csv",
    "Todas as Doenças": "Clustering/planilha/planilha_unificada_clusterizado.csv"
}

features = ["AREA_DESMATADA_KM2", "FRP", "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"]
target = "OBITOS"

# === Função para calcular RMSE com bootstrap ===
def bootstrap_rmse(model, X, y, n_iter=N_ITER):
    rmses = []
    for _ in range(n_iter):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        rmses.append(rmse)
    return np.array(rmses)

# === Loop nos grupos ===
for grupo, caminho in caminhos.items():
    print(f"\n📊 Análise Estatística - {grupo}")
    df = pd.read_csv(caminho)

    # Preparo
    df[target] = df[target].replace("-", np.nan)
    for col in features + [target]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df[features + [target]].copy()
    for col in features + [target]:
        df[col] = df[col].fillna(df[col].median())

    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])

    X = df[features]
    y = df[target]

    # === Gerar distribuições de RMSE ===
    modelo_lr = LinearRegression()
    modelo_rf = RandomForestRegressor(random_state=RANDOM_STATE)

    rmse_lr = bootstrap_rmse(modelo_lr, X, y)
    rmse_rf = bootstrap_rmse(modelo_rf, X, y)

    # === Intervalos de Confiança 95% ===
    ci_lr = np.percentile(rmse_lr, [2.5, 97.5])
    ci_rf = np.percentile(rmse_rf, [2.5, 97.5])

    print(f"\n📌 Intervalo de Confiança 95% (RMSE):")
    print(f"Linear Regression: [{ci_lr[0]:.4f}, {ci_lr[1]:.4f}]")
    print(f"Random Forest:     [{ci_rf[0]:.4f}, {ci_rf[1]:.4f}]")

    # === Teste de Hipóteses (t de Student pareado) ===
    stat, p_valor = ttest_rel(rmse_lr, rmse_rf)
    print(f"\n🧪 Teste de Hipótese (LR vs RF):")
    print(f"Estatística t = {stat:.4f}")
    print(f"p-valor = {p_valor:.4f}")
    
    if p_valor < 0.05:
        print("→ Diferença estatisticamente significativa (nível 5%)")
    else:
        print("→ Diferença **não** estatisticamente significativa (nível 5%)")


# -----------------------------
# Este código realiza a comparação entre os modelos Linear Regression e Random Forest 
# para cada grupo de doenças (Alta, Média, Baixa Sensibilidade e Todas as Doenças) por meio de:
# 
# 1. Intervalo de Confiança (IC 95%) para o RMSE:
#    → Informa a faixa de valores mais prováveis para o erro médio quadrático de cada modelo.
#    → Quanto menor e mais estreito o intervalo, mais confiável e preciso o modelo é.
# 
# 2. Teste de Hipóteses t pareado:
#    → Verifica se há diferença estatística entre os modelos comparando as distribuições de RMSE.
#    → Um p-valor < 0.05 indica que a diferença de desempenho entre os modelos é significativa.
#
# Interpretação prática:
# - Se a Regressão Linear tiver menor RMSE e a diferença for significativa, ela é preferível.
# - Se não houver diferença significativa, ambos os modelos se equivalem para aquele grupo.
# 
# Assim, este código ajuda a embasar a escolha dos modelos com testes estatísticos robustos.

# As análises foram feitas com 1000 iterações de bootstrap dos RMSEs
# para Linear Regression e Random Forest em 4 grupos: Alta, Média, Baixa Sensibilidade e Todas as Doenças.
#
# 1. Alta Sensibilidade:
# - Linear Regression apresentou RMSE médio menor e intervalo de confiança mais baixo.
# - O teste t indicou p-valor = 0.0000 → diferença estatisticamente significativa.
# Conclusão: Linear Regression é superior ao Random Forest neste grupo.
#
# 2. Média Sensibilidade:
# - Linear Regression também teve melhor desempenho médio e intervalo menor.
# - Teste t com p-valor = 0.0000 → diferença significativa.
# Conclusão: Linear Regression é estatisticamente superior neste grupo também.
#
# 3. Baixa Sensibilidade:
# - Random Forest teve menor RMSE médio, mas o teste t deu p-valor = 0.0819 (> 0.05).
# - Não há evidência estatística de superioridade entre os modelos.
# Conclusão: Ambos os modelos são viáveis, sem diferença estatística relevante.
#
# 4. Todas as Doenças (Clusterizado):
# - Linear Regression teve intervalo de confiança mais favorável.
# - Teste t com p-valor = 0.0000 → diferença estatisticamente significativa.
# Conclusão: Linear Regression é superior também nesta base geral.
#
# Conclusão Final:
# - Linear Regression foi estatisticamente superior ao Random Forest nos grupos:
#   Alta Sensibilidade, Média Sensibilidade e Todas as Doenças.
# - Para Baixa Sensibilidade, os dois modelos são equivalentes estatisticamente.
# - Linear Regression mostrou-se mais estável e confiável para este cenário de dados.