# 🔥 Impacto das Queimadas na Mortalidade por Doenças Respiratórias no Amazonas

## 🧭 Objetivo

Este projeto visa **investigar a relação entre queimadas e a mortalidade por doenças respiratórias no estado do Amazonas**, usando dados públicos de focos de incêndio e registros de óbitos. A partir de técnicas de pré-processamento e análise exploratória de dados, buscamos compreender como o aumento das queimadas pode influenciar a saúde respiratória da população.

---

## 📊 Análises Realizadas

1. **Correlação Temporal entre Queimadas e Óbitos Respiratórios**
   - Identificar se existe aumento simultâneo no número de focos de queimadas e óbitos por doenças respiratórias ao longo do tempo.
   - Avaliação mensal e anual dos dois fenômenos.

2. **Distribuição por Município**
   - Verificar **quais municípios concentram mais queimadas** e se estes coincidem com maior mortalidade respiratória.
   - Geração de mapas e gráficos regionais para visualização geográfica.

3. **Análise de Risco por Ano e Mês**
   - Detectar **períodos críticos do ano** com maior número de queimadas e óbitos.
   - Essa análise permite apoiar políticas públicas e ações de prevenção.

---

## 📁 Dados Utilizados

### 🟤 Base de Mortalidade (SIM - Ministério da Saúde)
- Registros de óbitos de 2023 no estado do Amazonas.
- Foco em causas respiratórias segundo a **CID-10** (J00 a J99).
- Campos importantes: `DTOBITO`, `CAUSABAS`, `CODMUNOCOR`, `SEXO`, `IDADE`.

### 🔥 Base de Queimadas (INPE - Programa Queimadas)
- Registros de focos de incêndio detectados via satélite no Amazonas (2023).
- Campos importantes: `DataHora`, `Municipio`, `Latitude`, `Longitude`, `FRP`, `Bioma`.

---

## 🛡️ Medidas de Proteção para a População

Com base nas análises, recomenda-se que **durante os meses de maior risco** (determinados pela combinação entre queimadas e mortalidade):

---

## 🧪 Metodologia

- Pré-processamento de dados com `pandas` e `datetime`.
- Filtragem de registros respiratórios (CID-10: J00 a J99).
- Conversão e padronização de campos temporais e geográficos.
- Análise estatística e visual com Python (`matplotlib`, `seaborn`, `folium`).

---

## 👩‍🔬 Autoria

- **Maria Isabel Nicolau (Bel)**  
- Projeto para Ciência de Dados Ambiental e Saúde Pública
