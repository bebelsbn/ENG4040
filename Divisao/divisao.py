import pandas as pd
import json

# Caminhos dos arquivos de entrada
csv_path = "planilha_unificada.csv"
json_path = "Sprint03/Divisao/doencas.json"

# Leitura da planilha principal (dados integrados de mortalidade, queimadas etc.)
df = pd.read_csv(csv_path, sep=';')

# Leitura do arquivo JSON que contém a divisão dos CIDs em categorias de sensibilidade (Alta, Média, Baixa)
with open(json_path, 'r', encoding='utf-8') as f:
    doencas = json.load(f)

# Função para converter faixas como "J40–J44" em tuplas ("J40", "J44")
def parse_faixa(faixa):
    return tuple(faixa.replace("–", "-").split("-"))

# Organiza as faixas de CID por nível de sensibilidade
# Justificativa: doenças respiratórias possuem diferentes níveis de associação com fatores ambientais como fumaça e PM2.5
# A segmentação por sensibilidade foi motivada por resultados do projeto que mostraram fracas correlações quando os dados eram analisados de forma agregada
faixas = {"Alta": [], "Média": [], "Baixa": []}
for item in doencas:
    categoria = item["categoria"].split()[0]  # extrai apenas "Alta", "Média" ou "Baixa"
    for entrada in item["dados"]:
        ini, fim = parse_faixa(entrada["cid"])
        faixas[categoria].append((ini, fim))

# Funções auxiliares para processar o código CID e verificar se ele pertence a uma faixa
def cid_para_int(cid):
    return int(cid[1:])

def pertence_a_faixa(cid, lista_faixas):
    try:
        if not cid or not isinstance(cid, str) or len(cid) < 3:
            return False
        letra, valor = cid[0], cid_para_int(cid)
        for ini, fim in lista_faixas:
            if letra == ini[0] and cid_para_int(ini) <= valor <= cid_para_int(fim):
                return True
    except:
        return False
    return False

# Classifica o CID puro em Alta, Média ou Baixa sensibilidade com base nas faixas definidas
def classificar_cid(cid):
    if pertence_a_faixa(cid, faixas["Alta"]):
        return "Alta"
    elif pertence_a_faixa(cid, faixas["Média"]):
        return "Média"
    elif pertence_a_faixa(cid, faixas["Baixa"]):
        return "Baixa"
    else:
        return "Desconhecida"

# Os CIDs na planilha original têm formato como "J44   Doença pulmonar obstrutiva crônica"
# Aqui extraímos apenas o código CID (ex: "J44"), para poder aplicar a lógica de faixa
df["CID_PURO"] = df["Categoria CID-10"].str.extract(r'^(J\d{2})')

# Aplicamos a função de classificação com base no CID puro
# Justificativa: a divisão permite análises mais específicas por grupo clínico e melhora o desempenho dos modelos
df["Sensibilidade"] = df["CID_PURO"].apply(classificar_cid)

# Gera e salva arquivos CSV segmentados por sensibilidade
# Justificativa: esses subconjuntos serão usados para criar modelos mais interpretáveis e eficazes para cada tipo de doença
df[df["Sensibilidade"] == "Alta"].to_csv("Sprint03/Divisao/planilha_alta.csv", index=False)
df[df["Sensibilidade"] == "Média"].to_csv("Sprint03/Divisao/planilha_media.csv", index=False)
df[df["Sensibilidade"] == "Baixa"].to_csv("Sprint03/Divisao/planilha_baixa.csv", index=False)

# Verificação adicional: quantos registros não foram classificados?
nao_classificados = df[df["Sensibilidade"] == "Desconhecida"]
if nao_classificados.empty:
    print("Todos os registros foram classificados com sucesso.")
else:
    print(f"Encontrados {len(nao_classificados)} registros sem classificação de sensibilidade.")
    print(nao_classificados[["Categoria CID-10", "CID_PURO"]].head(10))  # mostra exemplos

print("Arquivos gerados com sucesso!")
