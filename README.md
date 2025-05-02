# Amazônia em Chamas: Como o Desmatamento e os Incêndios Afetam a Saúde Respiratória no Amazonas

## 📄 Sobre o Projeto

Este projeto integra dados públicos para construir uma planilha unificada que correlaciona:
- Mortalidade por doenças respiratórias;
- Indicadores de queimadas (dias sem chuva, precipitação, risco de fogo, FRP);
- Área desmatada por município.

O objetivo é analisar os impactos ambientais e de saúde nas populações do estado do Amazonas, buscando revelar padrões temporais e espaciais entre desmatamento, incêndios e efeitos respiratórios.

O projeto se inspira em estudos recentes que mostram como queimadas e poluição atmosférica elevam hospitalizações, aumentam taxas de morbimortalidade e agravam condições pulmonares, especialmente em populações vulneráveis.

---

## 📂 Dados Utilizados

- `desmatamento.csv`: área desmatada anual por município.
- `mortalidade_unificada.csv`: mortes mensais por doenças respiratórias por município.
- `queimadas_unificadas.csv`: métricas mensais de queimadas por município (dias sem chuva, precipitação, risco de fogo, FRP).

Os dados foram integrados em uma única tabela final `planilha_unificada.csv`, contendo:
`ano`, `mês`, `município`, `óbito respiratório`, `dia sem chuva`, `precipitação`, `risco de fogo`, `FRP`, `área desmatada`.

---

## 🔍 Possíveis Análises

Com essa base integrada, você pode explorar:
- ✅ Séries temporais: há aumento de mortes nos meses com mais queimadas?
- ✅ Comparação por município: locais mais desmatados apresentam piores indicadores de saúde?
- ✅ Relação clima-incêndio: como dias sem chuva e risco de fogo impactam os padrões observados?
- ✅ Análises espaciais: mapeamento por região para identificar hotspots críticos de risco ambiental e sanitário.
- ✅ Modelagem: regressões para testar correlação entre variáveis ambientais e saúde.
- ✅ Correlação entre aumento de queimadas e picos de óbitos por doenças respiratórias.
- ✅ Comparação de períodos de seca vs. chuva para verificar variação em mortalidade (período seco mostrou até 3x mais internações​).
- ✅ Relação entre área desmatada acumulada e aumento progressivo de queimadas e impactos na saúde.
- ✅ Análise espacial: municípios mais afetados vs. menos afetados, normalizando pelo percentual desmatado em relação à área total.
- ✅ Comparação entre municípios urbanos (ex: Manaus) e rurais, considerando alertas ambientais e índices de poluição local​.
- ✅ Exploração do impacto das condições climáticas (dias sem chuva, risco de fogo) nas séries temporais de mortalidade.
- ✅ Sugestão para futuros modelos preditivos: uso de séries temporais para prever mortalidade a partir de variáveis ambientais.

---

## 💡 Inspiração do Estudo Original

O estudo acadêmico analisado destacou:
- Queimadas aumentam material particulado no ar, elevando internações e mortes por doenças pulmonares.
- Períodos secos (estiagem) agravam drasticamente os efeitos.
- Grupos vulneráveis (idosos, crianças, pessoas com doenças pré-existentes) são os mais afetados.
- A integração de dados ambientais e de saúde pública é essencial para orientar políticas e alertas preventivos.

---

## 📈 Próximos Passos


- ✔ Explorar agrupamentos (clustering) para identificar padrões ocultos.
- ✔ Gerar gráficos e mapas geográficos interativos.
- ✔ Testar modelos preditivos simples com base nos dados históricos.

---

