if (!requireNamespace("taxonomizr", quietly = TRUE)) install.packages("taxonomizr")
library(taxonomizr)

# Baixa names.dmp e nodes.dmp
getNamesAndNodes(".")           
getAccession2taxid(".")         

# Baixa e prepara os accession2taxid
# Usa os arquivos baixados
prepareDatabase(accessionFile = ".",          
  sqlFile = "accessionTaxa.sql",
  taxdumpFile = ".")
