import pandas as pd
import glob

# Pasta onde estão os arquivos
mortalidade_path = 'base_dados/mortalidade'

# Lista para guardar os DataFrames
mortalidade_list = []

# Ler e empilhar todos os arquivos mortalidade_*.csv
for file in glob.glob(f'{mortalidade_path}/mortalidade_*.csv'):
    year = int(file[-8:-4])
    print(f"Lendo {file} (ano {year})")
    df = pd.read_csv(file, sep=';', encoding='latin1')

    # Limpar e padronizar colunas
    df.columns = [col.strip().replace('"', '').replace('Munic�pio', 'Municipio').replace('Marco', 'Março') for col in df.columns]

    if 'Municipio' not in df.columns:
        raise ValueError(f"⚠ Erro: coluna 'Municipio' não encontrada no arquivo {file}.")

    df['Municipio'] = df['Municipio'].str.strip()
    df['Codigo_IBGE'] = df['Municipio'].str.split(' ').str[0]
    df['Municipio_Nome'] = df['Municipio'].str.split(' ').str[1:].str.join(' ').str.upper()

    # Derreter para formato longo
    df_melt = df.melt(id_vars=['Codigo_IBGE', 'Municipio_Nome'], 
                      value_vars=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                      var_name='Mes', value_name='Obitos')
    df_melt['Ano'] = year
    mortalidade_list.append(df_melt)

# Concatenar tudo
mortalidade_unificada = pd.concat(mortalidade_list, ignore_index=True)

# Garantir numérico
mortalidade_unificada['Obitos'] = pd.to_numeric(mortalidade_unificada['Obitos'], errors='coerce').fillna(0)

# Reordenar colunas
colunas_finais = ['Ano', 'Mes', 'Codigo_IBGE', 'Municipio_Nome', 'Obitos']
mortalidade_unificada = mortalidade_unificada[colunas_finais]

# Exportar para CSV
mortalidade_unificada.to_csv('mortalidade_unificada.csv', index=False, encoding='utf-8')
print("✅ Arquivo 'mortalidade_unificada.csv' criado com sucesso!")
