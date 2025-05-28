import pandas as pd
import glob

# Caminho dos arquivos de mortalidade
mortalidade_path = 'base_dados/mortalidade'

# Lista para armazenar DataFrames
mortalidade_list = []

# Colunas desejadas
colunas_desejadas = ['Categoria CID-10', 'Janeiro', 'Fevereiro', 'Março', 'Abril',
                     'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro',
                     'Dezembro']

# Processar todos os arquivos
for file in glob.glob(f'{mortalidade_path}/mortalidade_*.csv'):
    ano = int(file[-8:-4])
    print(f"🔄 Lendo {file} (ano {ano})")

    df = pd.read_csv(file, sep=';', encoding='latin1')

    # Padronizar nome das colunas
    df.columns = [col.strip().replace('"', '').replace('Munic�pio', 'Municipio').replace('Marco', 'Março') for col in df.columns]

    # Selecionar apenas as colunas desejadas
    if 'Categoria CID-10' not in df.columns:
        raise ValueError(f"⚠ Erro: coluna 'Categoria CID-10' não encontrada no arquivo {file}")

    colunas_presentes = [col for col in colunas_desejadas if col in df.columns]
    df_filtrado = df[colunas_presentes].copy()
    df_filtrado.insert(0, 'ANO', ano)

    mortalidade_list.append(df_filtrado)

# Concatenar tudo
mortalidade_unificada = pd.concat(mortalidade_list, ignore_index=True)

# Salvar como CSV
mortalidade_unificada.to_csv('PlanilhaUnificada/mortalidade_unificada.csv', index=False, encoding='utf-8')
print("✅ Planilha unificada criada com sucesso!")
