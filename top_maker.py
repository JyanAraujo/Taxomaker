# Script para filtrar dados de tx. Modificado 06/02/2025 por Marcelo Pires (real gangsta) e Jyan Araújo.
## WARNING

# '''
# Esse script foi pensado tendo em mente a utilização clássica de nomenclatura do servidor.
# Isto é: Nesta etapa, o script espera a clássica nomeação composta pelos três elementos, separadas por underline (_):
#     1) "tx", que sinaliza o csv como possuindo taxonomia completa após passar pelo taxonomizr
#     2) "nome da amostra", que sinaliza (obviamente), o nome da amostra
#     3) "Alvo Molecular", que sinaliza (igualmente obviamene), o alvo molecular deste blast

# Exemplos corretos: tx_MA14_cytb, tx_GGII_18S, tx_JAB_tpp, tx_PE_total;
# Exemplos errados: Absolutamente tudo que não for no modelo acima.;

# F.A.Q:

# P: "Ah Marcelo, mas se eu não respeitar essa regra, o código vai explodir?"
# R: Não sei. Não tentei. Recomendo que não tente também.

# Abraços!
# '''

# Importando bibliotecas
import pandas as pd # type: ignore
import os
import sys
import argparse
import openpyxl # type: ignore
import time
from datetime import datetime

# Total start time
total_start_time = datetime.now()

# Salvando os argumentos passados pelo usuário
parser = argparse.ArgumentParser(description="Argumentos")
parser.add_argument("--arquivo", type=str, required=True, help="Caminho para o arquivo de entrada (obrigatório)")
args = parser.parse_args()
arg_1 = args.arquivo

## Do argumento 1, extrairemos o nome do arquivo
nome_arquivo = arg_1.split('/')[-1] # Extraindo o nome original do arquivo.
partes = nome_arquivo.split("_") # Separando as três partes do nome original.
partes[0] = "tops" # Substituindo a primeira por tops, para sinalizar que passou por este processo.
nome_arquivo = "_".join(partes) # Juntando as partes uma vez separadas. Nome do arquivo atualizado.
partes = nome_arquivo.split(".") # Retirando o .csv
partes[1] = "xlsx" # aplicando o .xlsx
nome_arquivo = ".".join(partes) # Juntando as partes uma vez separadas. Nome do arquivo atualizado.
print(nome_arquivo)

# Tratando o banco de dados
print('Carregando Banco de Dados...')
start_time = datetime.now()
print("Horário de Início", start_time.strftime("%I:%M:%S"))
df = pd.read_csv(arg_1, on_bad_lines='skip', quoting=3) # Carregando o csv
df = pd.DataFrame(df) # Transformando em um DataFrame
print('Fim do carregamento.')
end_time = datetime.now()
print("Horário de Finalização", end_time.strftime("%I:%M:%S"))
print("Tempo de duração do trabalho: ", end_time - start_time)

## Nomeando as colunas
novas_colunas = [
    "qseqid", "sseqid", "pident", "lenght", "mismatch", "gapopen",
    "qstart", "qend", "sstart", "send", "evalue", "bitscore",
    "SuperKingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"
]

## Error handling
    #Estava dando um erro esquisito aqui nessa parte.
    #Aparentemente, na hora de gerar os "tx" alguns (não todos), vieram com uma nova coluna de index.
    #Isso fez com que houvessem 20 colunas em vez de 19, em alguns casos.
    #Pra prevenir bugs aleatórios, fiz esse leve error handling

try:
    df.columns = novas_colunas # Tentando renomear as colunas
except ValueError as e: # em caso de erro
    df = df.drop(df.columns[0], axis=1) # removendo a 1a coluna do dataframe (o bendito index bugado)
    df.columns = novas_colunas # Tentando renomear novamente
print("Dimensões do df antes do groupby (depois do drop_duplicates):", df.shape)

# Salvando apenas os cinco melhores resultados de cada read, baseado em bitscore
df = df.drop_duplicates(subset=["qseqid", "Species"], keep ="first") # Removendo espécies iguais com diversos resultados em uma mesma read
df1 = df.groupby("qseqid").apply(lambda x: x.nlargest(5, "bitscore")).reset_index(drop=True)
df2 = df.groupby("qseqid").apply(lambda x: x.nlargest(1, "bitscore")).reset_index(drop=True)

#Criando as análises de proporção:
df3 = df1["Species"].value_counts(dropna=False)
df3 = pd.DataFrame(df3)
df3["proportion"] = ((df3["count"] / df3["count"].sum()) * 100).round(2)
df4 = df2["Species"].value_counts(dropna=False)
df4 = pd.DataFrame(df4)
df4["proportion"] = ((df4["count"] / df4["count"].sum()) * 100).round(2)

# Salvando o dataframe
print('Salvando arquivo')
start_time = datetime.now()
print("Horário de Início", start_time.strftime("%I:%M:%S"))
with pd.ExcelWriter(nome_arquivo) as writer:
    df1.to_excel(writer, sheet_name= "Top_5")
    df3.to_excel(writer, sheet_name= "Proporção_5")
    df2.to_excel(writer, sheet_name= "Top_1")
    df4.to_excel(writer, sheet_name= "Proporção_1")
print('Arquivo salvo!')
end_time = datetime.now()
print("Horário de Finalização", start_time.strftime("%I:%M:%S"))
print("Tempo de duração do trabalho: ", end_time - start_time)
print("------------")
total_end_time = datetime.now()
print("Tempo total de duração do trabalho: ", total_end_time - total_start_time)