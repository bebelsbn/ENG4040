import pandas as pd

# Lista de arquivos e seus separadores
arquivos = {
    "planilha_unificada.csv": ";",  # separador usado na planilha unificada
    "Sprint03/Divisao/planilha_alta.csv": ",",
    "Sprint03/Divisao/planilha_media.csv": ",",
    "Sprint03/Divisao/planilha_baixa.csv": ","
}

# Itera sobre os arquivos e exibe as informações
for nome_arquivo, separador in arquivos.items():
    print(f"\n===== Analisando: {nome_arquivo} =====")
    try:
        df = pd.read_csv(nome_arquivo, sep=separador)

        # Exibe número de linhas e colunas
        print(f"Número de linhas: {df.shape[0]}")
        print(f"Número de colunas: {df.shape[1]}")

        # Exibe nomes das colunas
        print("Colunas:")
        print(df.columns.tolist())

        # Conta valores nulos por coluna
        nulos_por_coluna = df.isnull().sum()
        print("\nValores nulos por coluna:")
        print(nulos_por_coluna)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
