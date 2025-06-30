# =================== ANÁLISE DOS RESULTADOS ===================

# O que os gráficos mostram?
# Cada gráfico salvo na pasta Clustering/imagem mostra a separação dos dados em 3 clusters
# considerando as duas primeiras variáveis padronizadas: OBITOS e AREA_DESMATADA_KM2.
# As cores representam os clusters descobertos automaticamente pelo algoritmo.

# Interpretação das imagens:

# - **planilha_alta**: Os dados estão mais espalhados e o algoritmo conseguiu formar clusters visualmente distintos.
#   Isso sugere que, para doenças altamente sensíveis a fatores ambientais, como DPOC e asma,
#   há variações mais marcantes nos óbitos em função do desmatamento.

# - **planilha_media**: Apesar de uma leve separação, a maioria dos dados está concentrada em um mesmo grupo.
#   Isso pode indicar que doenças como pneumonia e infecções pulmonares possuem menos distinção clara
#   entre diferentes perfis ambientais, mas ainda assim há subgrupos relevantes.

# - **planilha_baixa**: Os dados estão fortemente concentrados no eixo com poucos óbitos,
#   e os clusters se sobrepõem mais, o que reflete menor sensibilidade dessas doenças a variáveis ambientais.

# - **planilha_unificada**: A junção de todas as categorias gera uma sobreposição considerável,
#   o que justifica a necessidade de divisão por sensibilidade — reforçando que a análise agregada pode mascarar padrões específicos.

# Conclusão:
# O clustering permitiu visualizar como as variáveis ambientais influenciam de forma diferenciada os óbitos,
# dependendo do tipo de doença. Esses agrupamentos podem ser usados futuramente para:
# - treinar modelos preditivos distintos por cluster;
# - fazer estudos direcionados para regiões mais críticas;
# - validar hipóteses sobre a associação entre queimadas e mortalidade respiratória.

# ==============================================================

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os

# Cria a pasta Clustering se ela não existir
os.makedirs("Clustering", exist_ok=True)

# Arquivos a processar e seus separadores
arquivos = {
    "planilha_unificada.csv": ";",
    "Divisao/planilha_alta.csv": ",",
    "Divisao/planilha_media.csv": ",",
    "Divisao/planilha_baixa.csv": ","
}

# Colunas numéricas relevantes para o clustering
colunas_numericas = [
    "OBITOS", "AREA_DESMATADA_KM2", "FRP",
    "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"
]

for nome_arquivo, separador in arquivos.items():
    print(f"\nClustering para: {nome_arquivo}")

    try:
        df = pd.read_csv(nome_arquivo, sep=separador)

        # Substitui valores inválidos "-" por NaN
        df[colunas_numericas] = df[colunas_numericas].replace("-", np.nan)
        df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric, errors='coerce')
        df_limpo = df.dropna(subset=colunas_numericas)

        # Padroniza os dados numéricos
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_limpo[colunas_numericas])

        # Aplica o KMeans
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        df_saida = df_limpo.copy()
        df_saida["Cluster"] = labels

        # Define nome base do arquivo
        base_nome = os.path.splitext(os.path.basename(nome_arquivo))[0]

        # Salva o CSV com os clusters
        caminho_csv = f"Clustering/planilha/{base_nome}_clusterizado.csv"
        df_saida.to_csv(caminho_csv, index=False)
        print(f"Planilha salva em: {caminho_csv}")

        # Salva gráfico dos clusters
        plt.figure(figsize=(6, 4))
        plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap="viridis", s=50)
        plt.title(f"Clusters - {base_nome}")
        plt.xlabel(colunas_numericas[0])
        plt.ylabel(colunas_numericas[1])
        plt.grid(True)
        plt.tight_layout()
        caminho_img = f"Clustering/imagem/{base_nome}_clusters.png"
        plt.savefig(caminho_img)
        plt.close()
        print(f"Gráfico salvo em: {caminho_img}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao processar {nome_arquivo}: {e}")
