
				          ---TAXOMAKER---
Criado por Jyan Araújo e Marcelo Pires

Esse é o topmaker, um software que une dois scripts anteriormente separados em um programa de fácil execução e rápido resultado.

O topmaker recebe como input um arquivo ".tab" vindo de um alinhamento com o programa blastn, e tem como output dois arquivos, um inicial ".csv" com associação taxonomica dos reads alinhados, e outro excel com 4 abas internas, top1, top5, proporção1 e proporção5.

					   ---OBJETIVO---

O arquivo top1 e top5 mostram a informação taxonômica de cada read alinhado com o banco de dados, onde top1 mostra o alinhamento de melhor score para cada read, e o top5 os 5 melhores alinhamentos. Nesse sentido proporção1 organiza os dados quanto ao valor relativo dos táxons (em %) para o top1, e para o top5 no proporção5.

					----Instalações----

Para rodar o programa são requeridas algumas instalações prévias. 

1- Instalação do Python

sudo apt update
sudo apt install python3 python3-pip -y

2- Instalação de pacotes usados nos scripts em Python

pip install rpy2
pip install pandas
pip install argparse
pip install openpyxl

3- Instalação do R

sudo apt update
sudo apt install -y r-base
apt install r-cran-littler

4- Instalação do banco de dados para accession

Uma das etapas mais importantes do programa é a associação taxonomica de cada linha do arquivo ".tab". Isso é feito a partir dos IDs (geralmente a segunda coluna do .tab) que de acordo com o banco de dados do ncbi é possível pegar os nomes dos taxons (dominio a espécie). Para isso é necessário baixar 3 arquivos e montar o banco de dados localmente. 

Para fazer tudo dessa etapa basta rodar o programa data_base_accession.r


Rscript data_base_accession.r 


				    ---Uso do taxomaker---

A tabela de input precisa necessariamente conter as seguintes colunas:

qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle

Que são definidas no argumento -outfmt "" do blastn

Ou seja, se o .tab vier com um numero de colunas diferente de 13, o programa vai dar erro. Se as informações estiverem desalinhadas com o que cada coluna representa, o programa pode rodar, mas criará tabelas erradas, então revise o conteúdo do resultado do blastn.

É possivel rodar o programa com:

python topmaker.py

Ele vai perguntar o caminho dos: Arquivo.tab, accessionTaxa.sql (banco de dados), e saída do arquivo.


OBS: Pretendemos fazer melhorias e (talvez) uma interface gráfica. Qualquer bug me chama!!! :D
 
