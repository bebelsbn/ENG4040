
# 🌿 Amazônia em Chamas: Como o Desmatamento e as Queimadas Afetam a Saúde Respiratória em Manaus

## 📄 Sobre o Projeto

Este projeto integra dados públicos para analisar a relação entre variáveis ambientais (como desmatamento e queimadas) e a mortalidade por doenças respiratórias no município de **Manaus**, entre 2020 e 2023.

A base consolidada reúne:
- Dados mensais de mortalidade respiratória (CID-10);
- Indicadores ambientais: dias sem chuva, precipitação, risco de fogo, FRP;
- Dados de qualidade do ar (PM2.5) coletados por sensores públicos em Manaus;
- Estimativas mensais de área desmatada com base no perfil do Amazonas.

O objetivo central é **identificar padrões temporais e ambientais associados ao aumento de mortes respiratórias**, com foco na população urbana mais exposta à poluição gerada pelas queimadas.

---

## 📂 Dados Utilizados

- `mortalidade_unificada.csv`: mortes mensais por doenças respiratórias (dados do SIM/DATASUS).
- `queimadas_unificadas.csv`: agregações mensais por satélite (dias sem chuva, risco de fogo, FRP).
- `desmatamento_mensal_amazonas.csv`: área desmatada, estimada por perfil proporcional mensal.
- `qualidade_ar_pm25.csv`: concentrações mensais de PM2.5 em Manaus (dados do PurpleAir).

**Planilha final integrada:** `planilha_unificada.csv`, com as colunas:

```
ano;Categoria CID-10;mes;OBITOS;AREA_DESMATADA_KM2;FRP;
RISCOFOGO;PRECIPITACAO;DIASEMCHUVA;pm2.5_atm;QUALIDADE_AR_CLASSIFICADA
```

---

## 🔍 Possibilidades de Análise

Com essa base unificada, o projeto viabiliza análises como:

- 📉 **Tendência temporal de mortalidade:** Há aumento de óbitos em meses com pior qualidade do ar?
- 🌫️ **Correlação entre PM2.5 e mortes respiratórias:** Qual o impacto da poluição atmosférica?
- 🔥 **Relação entre seca e queimadas:** Dias sem chuva se associam a risco de fogo e FRP elevados?
- 📊 **Modelos de regressão supervisionada:** Prever número de óbitos com base nas variáveis ambientais.
- 📆 **Análise sazonal:** Períodos secos mostram picos de mortalidade? Existe um padrão cíclico anual?
- 🧪 **Importância de variáveis:** Quais fatores ambientais mais explicam os óbitos em Manaus?
- 📌 **Classificação da qualidade do ar:** Categorias como "ruim" e "muito ruim" estão associadas a maiores médias de óbitos?
- 📈 **Construção de série temporal:** Modelos que preveem mortalidade com base em dados de meses anteriores.

---

## 💡 Base Teórica e Relevância

Inspirado em estudos recentes, este projeto parte de evidências de que:
- As queimadas elevam significativamente os níveis de material particulado (PM2.5).
- O aumento da poluição está associado a picos de internações e mortes, sobretudo entre idosos e crianças.
- A análise integrada de dados ambientais e de saúde é crucial para orientar políticas públicas, sistemas de alerta e ações preventivas.

---

## 🚀 Próximos Passos

- ✔ Ampliar os testes com modelos preditivos (Random Forest, XGBoost).
- ✔ Avaliar regressões segmentadas por categoria CID-10.
- ✔ Explorar mais séries temporais e lags (efeitos retardados).
- ✔ Construir dashboards interativos para visualização pública.
- ✔ Comparar padrões de 2020-2023 com séries históricas mais longas, se disponíveis.
