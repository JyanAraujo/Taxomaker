#Esse programa realiza a associação taxonômica a partir do taxaID da saída blastn, a partir de um 
#banco de dados SQL --> accessions_taxa.sql


#Função para instalar e carregar pacotes (usada apenas uma vez)
options(repos = c(CRAN = "https://cran.r-project.org/"))
if (!requireNamespace("taxonomizr", quietly = TRUE)) install.packages("taxonomizr")
if (!requireNamespace("readxl", quietly = TRUE)) install.packages("readxl")

#carregando pacotes
library(taxonomizr)
library(readxl)

#Pega argumento do main.py
args <- commandArgs(trailingOnly = TRUE)
file_path1 <- args[1]

#Estabelecendo nome base para salvar arquivo
file_name <- basename(file_path1)
save_name <- gsub(".tab$", "", file_name)
save_path <- paste0("tx_", save_name, ".csv")

#Lendo .tab
df <- read.table(file_path1, sep = "\t", stringsAsFactors = FALSE)

#Extrai id que o accession vai ler (adaptado a dois tipos de estrutura de id)
accessions <- sapply(strsplit(df[,2], "\\|"), function(x) {
  if (length(x) >= 3) return(x[3]) else return(x[1])
})
df$V2 <- accessions

#Argumento no main.py
accession_path <- args[2]

#Associando taxonomia
taxaId <- accessionToTaxa(accessions, accession_path)
df$taxa <- getTaxonomy(taxaId, accession_path)

#Remove col v13
if (ncol(df) >= 13) df$V13 <- NULL

#Renomeando colunas
colnames(df) <- c(
  "qseqid", "sseqid", "pident", "length", "mismatch", "gapopen",
  "qstart", "qend", "sstart", "send", "evalue", "bitscore", "taxa"
)[1:ncol(df)]

#Salvando como .csv
save_path <- args[3]
write.csv(df, save_path, row.names = FALSE)


