# -------------------------------------------------------------------------------------------
# AVALIAÇÃO DO DESEMPENHO COM VALIDAÇÃO CRUZADA (K-Fold e LOOCV)
#
# Objetivo:
# Avaliar a robustez e a estabilidade dos modelos Random Forest por meio de técnicas de 
# validação cruzada, comparando o desempenho preditivo (RMSE e R²) entre os conjuntos 
# clusterizado e divididos por sensibilidade (Alta, Média e Baixa).
#
# Importância no trabalho:
# A validação cruzada permite verificar a generalização dos modelos e identificar 
# possíveis overfittings ou variações de desempenho entre diferentes subconjuntos.
# Além disso, fornece métricas mais confiáveis e independentes do particionamento aleatório.
#
# Etapas realizadas:
# - Leitura das planilhas de entrada com separadores diferentes.
# - Limpeza e transformação das variáveis (incluindo codificação de variáveis categóricas).
# - Aplicação de validação cruzada K-Fold (10 folds) para cálculo de RMSE e R² médios.
# - Aplicação opcional do LOOCV (Leave-One-Out) quando a base possui ≤ 500 amostras.
# - Geração automática de gráficos boxplot para visualização da dispersão das métricas.
#
# Observações:
# - A métrica RMSE é invertida na função de scoring (por padrão do scikit-learn).
# - A LOOCV é omitida em bases grandes por inviabilidade computacional.
# -------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, LeaveOneOut, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.preprocessing import StandardScaler
import warnings
import matplotlib.pyplot as plt

# Função de erro RMSE
def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

rmse_scorer = make_scorer(rmse, greater_is_better=False)

arquivos = {
    "Clustering/planilha/planilha_unificada_clusterizado.csv": ";",
    "Divisao/planilha_alta.csv": ",",
    "Divisao/planilha_media.csv": ",",
    "Divisao/planilha_baixa.csv": ","
}

model = RandomForestRegressor(random_state=42)

for caminho, sep in arquivos.items():
    print(f"\n📁 Avaliando: {caminho}")

    try:
        df = pd.read_csv(caminho, sep=sep)

        if 'OBITOS' not in df.columns:
            print(f"⚠️  A coluna 'OBITOS' não foi encontrada no arquivo: {caminho}")
            continue

        # Limpeza e conversão
        df = df[df['OBITOS'].apply(lambda x: str(x).replace(',', '.').replace('-', '').replace(' ', '').replace('.', '', 1).isdigit())]
        df['OBITOS'] = df['OBITOS'].astype(float)

        y = df['OBITOS']
        X = df.drop(columns=['OBITOS'])

        # Codificação e normalização
        X = pd.get_dummies(X, drop_first=True)
        X = StandardScaler().fit_transform(X)

        # Validação cruzada K-Fold
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        rmse_scores_kfold = cross_val_score(model, X, y, cv=kf, scoring=rmse_scorer)
        r2_scores_kfold = cross_val_score(model, X, y, cv=kf, scoring='r2')

        print("🔁 K-Fold (10):")
        print(f"   RMSE médio: {-np.mean(rmse_scores_kfold):.2f}")
        print(f"   R² médio:   {np.mean(r2_scores_kfold):.3f}")

        # LOOCV com apenas RMSE
        if len(df) <= 500:
            loo = LeaveOneOut()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                rmse_scores_loo = cross_val_score(model, X, y, cv=loo, scoring=rmse_scorer)
            print("🔁 Leave-One-Out (LOOCV):")
            print(f"   RMSE médio: {-np.mean(rmse_scores_loo):.2f}")
            print(f"   R² médio:   ⚠️ Não avaliado por ser indefinido no LOOCV")
        else:
            print("⚠️  LOOCV não executado devido ao tamanho da base.")

        # Gráfico da validação cruzada
        rmse_individual = -rmse_scores_kfold
        r2_individual = r2_scores_kfold

        plt.figure(figsize=(10, 5))
        plt.boxplot([rmse_individual, r2_individual], labels=['RMSE', 'R²'])
        plt.title(f'Validação Cruzada - {caminho.split("/")[-1]}')
        plt.ylabel('Valor da Métrica')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'validacao_{caminho.split("/")[-1].replace(".csv", "")}.png', dpi=300)
        plt.show()

    except Exception as e:
        print(f"❌ Erro ao processar {caminho}: {e}")
