# 🌿 Amazônia em Chamas: Como o Desmatamento e as Queimadas Afetam a Saúde Respiratória em Manaus

## 📄 Sobre o Projeto

Este projeto de Ciência de Dados investiga a relação entre **variáveis ambientais** (desmatamento, queimadas, qualidade do ar) e a **mortalidade por doenças respiratórias** na cidade de **Manaus**, no período de **2020 a 2023**.

Por meio da unificação de dados públicos, modelagem preditiva e análise estatística, buscamos **identificar padrões e fatores críticos** que influenciam os óbitos causados por doenças respiratórias, especialmente durante os períodos mais secos e com maior atividade de queimadas.

## Dados Utilizados

- `mortalidade_unificada.csv`: óbitos mensais por categoria CID-10 respiratória (SIM/DATASUS).
- `queimadas_unificadas.csv`: variáveis ambientais derivadas de satélite (dias sem chuva, FRP, risco de fogo).
- `desmatamento_mensal_amazonas.csv`: estimativa da área desmatada no AM (INPE/PRODES).
- `qualidade_ar_pm25.csv`: média mensal de concentração de PM2.5 (PurpleAir – sensores urbanos de Manaus).

**Planilha integrada final:** `planilha_unificada.csv`  
Colunas principais:
```
ano;Categoria CID-10;mes;OBITOS;AREA\_DESMATADA\_KM2;FRP;
RISCOFOGO;PRECIPITACAO;DIASEMCHUVA;pm2.5\_atm;QUALIDADE\_AR\_CLASSIFICADA
```


## Etapas e Análises Realizadas

### Pré-processamento e Segmentações
- Tratamento de valores ausentes com imputação por mediana.
- Normalização (StandardScaler) das variáveis preditoras.
- Separação dos dados em:
  - **Alta, Média e Baixa Sensibilidade**, com base em categorias CID-10.
  - **Agrupamento por cluster** de similaridade entre doenças respiratórias.

---

### 🤖 Modelos de Regressão Treinados

Modelos testados:
- Regressão Linear
- Random Forest
- Árvore de Regressão (DecisionTreeRegressor)
- XGBoost Regressor

Avaliação com:
- RMSE (Root Mean Squared Error)
- R² (Coeficiente de Determinação)

**Comparações feitas com e sem pré-processamento** (normalização + imputação).

###  Análise Estatística

Para cada grupo (Alta, Média, Baixa Sensibilidade e Todas as Doenças), foram realizados:

- **Intervalos de Confiança (95%)** para o RMSE usando bootstrap (n = 1000)
- **Testes de Hipóteses (t pareado)** para verificar se o Random Forest superava estatisticamente a Regressão Linear

**Exemplo – Alta Sensibilidade:**
```

Intervalo de Confiança (95%) para RMSE:
LR: \[3.0857, 5.1354]
RF: \[3.6094, 5.6144]

Teste t pareado:
t = -22.29 | p-valor = 0.0000 → diferença significativa

```

---

### 🎯 Importância das Variáveis

Para cada modelo:
- Regressão Linear → coeficientes padronizados
- Random Forest → feature importance

Fatores como **FRP**, **pm2.5** e **dias sem chuva** destacaram-se como variáveis com maior influência sobre os óbitos.

---

### 📌 Análise por CID-10

As doenças com menor erro de previsão (melhor RMSE) foram:
- Asma (J45) – RMSE: 0.57
- Bronquiolite (J21) – RMSE: 0.73
- Edema pulmonar (J81) – RMSE: 0.81

Pneumonias (J12, J15, J18) apresentaram alto erro, sugerindo maior complexidade ou menor correlação com os fatores ambientais utilizados.


## Modelo Final Recomendado

**Modelo Escolhido:** Random Forest com pré-processamento  
**Justificativa:**
- Melhor desempenho em RMSE e R² em todos os grupos avaliados.
- Resultados estatisticamente significativos na maioria dos testes.
- Capacidade de capturar interações não-lineares.
- Robustez e estabilidade (menor variância de resultados).

---

##  Possibilidades de Análise

- Análise sazonal e de tendência: Padrões cíclicos em meses secos.
- Importância de variáveis ambientais nas mortes respiratórias.
- Previsão de óbitos com base nas variáveis climáticas.
- Exploração por CID-10 e por município.
- Expansão para séries temporais com lag e efeitos acumulados.

---

## Relevância Social

A relação entre desmatamento e saúde pública é urgente. Este projeto oferece:

- Subsídios para políticas de controle ambiental;
- Geração de alertas baseados em variáveis críticas;
- Apoio à atuação de gestores públicos em saúde e meio ambiente.

