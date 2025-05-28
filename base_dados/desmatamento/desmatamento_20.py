import pandas as pd

# 1. Carregar todos os dados mensais do Amazonas (com todos os anos)
df_amazonas = pd.read_csv("desmatamento_mensal_amazonas.csv", sep=";")

# 2. Carregar os dados anuais de Manaus
df_manaus = pd.read_csv("desmatamento_anual_manaus.csv", sep=",")
df_manaus.columns = ["year", "areakm", "municipality", "geocode_ibge", "state"]
df_manaus["year"] = df_manaus["year"].astype(int)
df_manaus["areakm"] = df_manaus["areakm"].astype(float)

# 3. Anos a processar
anos = [2020, 2021, 2022, 2023]

for ano in anos:
    # Filtrar apenas o ano desejado e tipo DESMATAMENTO
    df_am_ano = df_amazonas[
        (df_amazonas["year"] == ano) &
        (df_amazonas["className"].str.contains("DESMATAMENTO", case=False))
    ]

    # Agrupar por mês e calcular perfil proporcional
    df_mensal = df_am_ano.groupby("month", as_index=False)["area"].sum()
    total = df_mensal["area"].sum()

    # Se não há dados para o ano, pula
    if total == 0 or df_mensal.empty:
        print(f"Aviso: Sem dados de desmatamento para o Amazonas no ano {ano}. Pulando...")
        continue

    df_mensal["peso_mensal"] = df_mensal["area"] / total

    # Obter área anual de Manaus
    area_manaus = df_manaus[df_manaus["year"] == ano]["areakm"].values
    if len(area_manaus) == 0:
        print(f"Aviso: Ano {ano} não encontrado no CSV de Manaus. Pulando...")
        continue

    area_total = area_manaus[0]

    # Aplicar perfil ao valor de Manaus
    df_mensal["ANO"] = ano
    df_mensal["AREA_DESMATADA_KM2"] = df_mensal["peso_mensal"] * area_total

    # Selecionar e renomear colunas
    df_resultado = df_mensal[["ANO", "month", "AREA_DESMATADA_KM2"]]
    df_resultado.columns = ["ANO", "MES", "AREA_DESMATADA_KM2"]

    # Salvar resultado
    nome_arquivo = f"estimativa_manaus_mensal_{ano}.csv"
    df_resultado.to_csv(nome_arquivo, index=False)
    print(f"✅ Arquivo salvo: {nome_arquivo}")
