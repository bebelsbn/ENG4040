import pandas as pd

# Carregar os dados
df = pd.read_csv('planilha_unificada.csv')

# Variáveis a categorizar
variables = ['deaths', 'DiaSemChuva', 'Precipitacao', 'RiscoFogo', 'FRP', 'area_desmatada_km2']
municipio_col = 'municipality'

# Definir faixas genéricas (você pode ajustar conforme os dados reais)
bins_dict = {
    'deaths': [0, 1, 10, 50, 100, 500],
    'DiaSemChuva': [0, 5, 10, 15, 20, 30],
    'Precipitacao': [0, 1, 5, 10, 15, 20],
    'RiscoFogo': [0, 0.1, 0.3, 0.5, 0.7, 1],
    'FRP': [0, 10, 30, 60, 100, 150],
    'area_desmatada_km2': [0, 1, 5, 10, 20, 50]
}

# Criar e salvar tabelas de frequência por município e categoria
for var in variables:
    df[f'{var}_cat'] = pd.cut(df[var], bins=bins_dict[var], include_lowest=True)
    freq_table = df.groupby([municipio_col, f'{var}_cat']).size().reset_index(name='Frequência')
    
    print(f"\nTabela de Frequência por Município – {var.capitalize()}:\n")
    print(freq_table.to_string(index=False))
    
    # Salvar em CSV para o relatório
    freq_table.to_csv(f'tabela_frequencia_{var}.csv', index=False)
