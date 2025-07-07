# -------------------------------------------------------------------------------------------
# ANÁLISE EXPLORATÓRIA DAS PLANILHAS
#
# Objetivo:
# Realizar uma análise estatística descritiva das variáveis numéricas presentes nas
# planilhas utilizadas no projeto, incluindo avaliação de valores ausentes (missing),
# medidas de tendência central, dispersão e percentis.
#
# Importância no trabalho:
# Esta etapa é fundamental para compreender a qualidade dos dados, identificar possíveis
# problemas (como muitos valores faltantes, outliers ou variáveis constantes), e orientar
# decisões nas etapas de pré-processamento e modelagem.
#
# Etapas realizadas:
# - Leitura de diferentes planilhas com separadores distintos.
# - Conversão robusta das colunas numéricas (tratando erros e valores não numéricos).
# - Cálculo das principais estatísticas: média, mediana, desvio padrão, variância, 
#   percentis, contagem e proporção de valores ausentes.
# - Impressão organizada das tabelas de estatísticas para cada conjunto de dados.
#
# Observações:
# - As estatísticas são arredondadas para duas casas decimais para facilitar leitura.
# - O código lida com exceções de forma robusta, informando caso um arquivo esteja ausente.
# -------------------------------------------------------------------------------------------

import pandas as pd

# Lista de arquivos e seus separadores
arquivos = {
    "planilha_unificada.csv": ";",
    "Divisao/planilha_alta.csv": ",",
    "Divisao/planilha_media.csv": ",",
    "Divisao/planilha_baixa.csv": ","
}

# Colunas numéricas que serão analisadas
cols_numericas = [
    "OBITOS", "AREA_DESMATADA_KM2", "FRP",
    "RISCOFOGO", "PRECIPITACAO", "DIASEMCHUVA", "pm2.5_atm"
]

# Loop por cada planilha
for nome_arquivo, separador in arquivos.items():
    print(f"\n===== Analisando: {nome_arquivo} =====")

    try:
        # Lê o arquivo
        df = pd.read_csv(nome_arquivo, sep=separador)

        # Converte as colunas numéricas para float (coerce = coloca NaN em erros)
        df[cols_numericas] = df[cols_numericas].apply(pd.to_numeric, errors='coerce')

        # Calcula estatísticas
        estatisticas = df[cols_numericas].describe().T
        estatisticas["variancia"] = df[cols_numericas].var()
        estatisticas["mediana"] = df[cols_numericas].median()
        estatisticas["missing"] = df[cols_numericas].isnull().sum()
        estatisticas["missing_%"] = (estatisticas["missing"] / len(df)) * 100
        estatisticas["count"] = df[cols_numericas].count()

        # Reorganiza as colunas na ordem desejada
        estatisticas = estatisticas[[
            "count", "missing", "missing_%", "mean", "std",
            "variancia", "min", "25%", "mediana", "50%", "75%", "max"
        ]]

        # Mostra as estatísticas
        print(estatisticas.round(2))

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao processar {nome_arquivo}: {e}")
