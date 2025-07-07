# -------------------------------------------------------------------------------------------
# ANÁLISE TEMPORAL DE ÓBITOS E INDICADORES AMBIENTAIS (ALTA SENSIBILIDADE)
#
# Objetivo:
# Avaliar a evolução mensal dos óbitos por doenças respiratórias de Alta Sensibilidade 
# e sua relação com fatores ambientais como queimadas (FRP), desmatamento, dias sem chuva 
# e concentração de PM2.5.
#
# Importância no trabalho:
# Esta visualização permite entender **padrões sazonais** e possíveis **correlações visuais**
# entre aumento de poluentes ou seca e elevação nos óbitos. Isso subsidia hipóteses sobre
# os períodos de maior risco e reforça a motivação para políticas públicas específicas em 
# determinadas épocas do ano.
#
# Etapas realizadas:
# - Leitura da planilha segmentada por sensibilidade
# - Conversão do campo "mês" para nome legível
# - Agrupamento dos dados por mês (somando óbitos e fazendo média dos fatores ambientais)
# - Geração de gráfico de linha comparando as curvas de óbitos e variáveis ambientais
# -------------------------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# Lê a planilha
df = pd.read_csv('Divisao/planilha_alta.csv')

# Converte OBITOS para número (substitui "-" por NaN)
df['OBITOS'] = pd.to_numeric(df['OBITOS'], errors='coerce')

# Filtra apenas os dados de doenças com Sensibilidade Alta
df = df[df['Sensibilidade'] == 'Alta']

# Converte mês de número para nome
meses_nomes = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
    5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
    9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}
df['mes_nome'] = df['mes'].map(meses_nomes)

# Agrupa por mês (caso tenha mais de uma linha por mês)
df_agrupado = df.groupby('mes_nome').agg({
    'OBITOS': 'sum',
    'FRP': 'mean',
    'AREA_DESMATADA_KM2': 'mean',
    'DIASEMCHUVA': 'mean',
    'pm2.5_atm': 'mean'
}).reset_index()

# Ordena os meses corretamente
ordem_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
               'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
df_agrupado['mes_nome'] = pd.Categorical(df_agrupado['mes_nome'], categories=ordem_meses, ordered=True)
df_agrupado = df_agrupado.sort_values('mes_nome')

# Cria o gráfico
plt.figure(figsize=(12, 6))
plt.plot(df_agrupado['mes_nome'], df_agrupado['OBITOS'], label='Óbitos (Alta Sensibilidade)', marker='o', linewidth=2)
plt.plot(df_agrupado['mes_nome'], df_agrupado['FRP'], label='Queimadas (FRP)', linestyle='--')
plt.plot(df_agrupado['mes_nome'], df_agrupado['AREA_DESMATADA_KM2'], label='Área Desmatada (km²)', linestyle='--')
plt.plot(df_agrupado['mes_nome'], df_agrupado['DIASEMCHUVA'], label='Dias sem chuva', linestyle='--')
plt.plot(df_agrupado['mes_nome'], df_agrupado['pm2.5_atm'], label='PM2.5 (µg/m³)', linestyle='--')

# Personalização
plt.title('Óbitos por Doenças Respiratórias de Alta Sensibilidade vs Indicadores Ambientais')
plt.xlabel('Mês')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
