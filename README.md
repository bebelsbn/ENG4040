# 🌿 Impacto das Queimadas na Mortalidade por Doenças Respiratórias no Estado do Amazonas: Uma Análise com Dados de 2023

## 📌 Descrição do Projeto

Este projeto tem como objetivo investigar a relação entre a ocorrência de queimadas e a mortalidade por doenças respiratórias no estado do Amazonas no ano de 2023. A análise utiliza duas bases de dados principais:

- **Base de Queimadas:** contendo registros dos focos ativos de incêndio no estado do Amazonas.
- **Base de Mortalidade:** contendo registros de óbitos, incluindo a causa básica do óbito (campo `CAUSABAS`) conforme codificação CID-10.

## 🧾 CID-10: Doenças Respiratórias Relevantes

Foi realizado um estudo para identificação dos códigos da Classificação Internacional de Doenças (CID-10) relacionados às doenças respiratórias com maior potencial de agravamento devido à poluição gerada por queimadas. Os seguintes grupos foram considerados:

- `J00–J06`: Infecções agudas das vias aéreas superiores (rinite, laringite, sinusite, etc.)
- `J12–J18`: Pneumonias
- `J20–J22`: Outras infecções respiratórias agudas das vias inferiores
- `J40–J47`: Doenças respiratórias obstrutivas crônicas (bronquites, asma, DPOC)
- `J00–J99`: Intervalo completo de doenças respiratórias (utilizado como filtro geral)

## 🎯 Objetivo da Análise

Avaliar a existência de correlação temporal e espacial entre:

- O número de focos de queimadas registrados no Amazonas;
- E o número de óbitos causados por doenças respiratórias (com base no CID-10).

## 🧪 Metodologia

1. **Filtragem dos dados de mortalidade** para manter apenas os óbitos com causa básica (CAUSABAS) no intervalo `J00–J99`.
2. **Tratamento e limpeza das datas** para alinhamento temporal entre as duas bases.
3. **Análise exploratória e visualização** dos dados por região, mês e tipo de doença.
4. **Avaliação de correlação estatística** entre a quantidade de queimadas e a mortalidade por doenças respiratórias.

## 📁 Estrutura dos Dados

### Base de Mortalidade (exemplo de colunas relevantes)

- `DTOBITO`: Data do óbito
- `CAUSABAS`: Causa básica do óbito (CID-10)
- `CODMUNOCOR`: Código do município de ocorrência
- `SEXO`, `IDADE`, `RACACOR`, `ESC`: Variáveis demográficas

### Base de Queimadas

- `data`: Data do foco
- `estado`, `municipio`: Localização
- `latitude`, `longitude`: Coordenadas
- `satélite`, `bioma`, `tipo_foco`: Metadados ambientais

## 📈 Resultados Esperados

- Gráficos temporais com a evolução de queimadas e óbitos por doenças respiratórias
- Análises de correlação entre os eventos ambientais e os efeitos na saúde
- Identificação de períodos críticos de atenção à saúde pública no Amazonas

## 👩‍🔬 Contribuição

Este projeto visa contribuir para a compreensão dos efeitos ambientais na saúde da população amazônica, auxiliando gestores públicos e pesquisadores na formulação de políticas preventivas e campanhas de conscientização.

---



