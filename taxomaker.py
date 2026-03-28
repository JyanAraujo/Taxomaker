#!/usr/bin/env

#O programa vai pegar um input (uma tabela de saída de um blatn)
#Vai passar pelo script taxonomizr.R e o resultado passar no top_maker.py
#Teremos como output 5 tabelas: 1-Resultado do taxonomizr.R, 2-top5, 3-top1, 
#4-proporcao5, 5- proporcao1

import subprocess as sb
import rpy2 as rp
import os

print("Bem vindo ao Taxo Maker :D !!! \n Vamos pegar sua tabela do blast e tratá-las para análises posteriores\n")
print("Autores: Marcelo Pires e Jyan Araújo > LPIP > IOC")

file_path1 = input("\nCopie o caminho do arquivo .tab e cole abaixo.\nLembrando que no Windows o separador é '/'\n")
accession_path = input("\nCopie o caminho do banco de dados .sql e cole abaixo. \n")
saida_path = input("\nEscreva o caminho de saída do arquivo .csv. \n")
blast_name = os.path.basename(file_path1).replace(".tab", "")
save_path = os.path.join(saida_path, f"tx_{blast_name}.csv")

print("\nAssociando Taxonomia...")

sb.run(["C:/Program Files/R/R-4.3.1/bin/x64/Rscript.exe", "./taxonomizr.R", file_path1, accession_path, save_path])

print("arquivo .csv gerado na pasta do programa\n\n")

print("Criando tops e proporções...")

sb.run(["python", "top_maker.py", "--arquivo", save_path])





