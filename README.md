# 1. Problema de Negócio

A empresa Fome Zero é um marketplace de restaurantes. Ou seja, seu core

business é facilitar o encontro e negociações de clientes e restaurantes. Os

restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza

informações como endereço, tipo de culinária servida, se possui reservas, se faz

entregas e também uma nota de avaliação dos serviços e produtos do restaurante,

dentre outras informações.

O projeto consiste em um dashboard estratégico e  interativo, gerado a partir de análises de 

dados da empresa, com o intuito de responder às principais perguntas de negócio que 

auxiliem o CEO da Fome Zero na tomada das melhores decisões estratégicas, visando alavancar 

ainda mais a empresa.

# 2. Premissas assumidas para a análise

1. O projeto e as análises foram construídos a partir de dados públicos disponíveis na plataforma Kaggle.
2. O modelo de negócio assumido foi de uma plataforma de marketplace.
3. As 4 principais visões gerenciais assumidas foram: Visão geral, visão países, visão cidades e visão tipos de culinária.

# 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as principais métricas das quatro visões gerenciais do modelo de negócio da empresa: 

1. Visão geral e global da empresa.
2. Visão dos países atendidos pela empresa.
3. Visão das cidades cadastradas na plataforma.
4. Visão dos tipos culinários existentes dos restaurantes cadastrados.

Cada visão é representada pelos principais conjuntos de métricas:

## Visão Geral

1. Quantidade de restaurantes cadastrados.
2. Quantidade de Países cadastrados.
3. Quantidade de cidades registradas.
4. Avaliações cadastradas na plataforma.
5. Tipos de culinária cadastradas.
6. Visualização global, contendo as informações básicas, dos restaurantes cadastrados.

## Visão Países

1. Quantidade de restaurantes por país.
2. Quantidade de cidades registradas por país.
3. Média das avaliações feitas por país.
4. Média de um prato para dois por país.

## Visão Cidades

1. Top 10 cidades com mais restaurantes cadastrados.
2. Top 7 cidades com restaurantes com avaliação maior que 4,0.
3. Top 7 cidades com restaurantes com avaliação menor que 2,5.
4. Top 10 cidades com mais restaurantes com tipos de culinária distintos.

## ****Visão Tipos Culinários****

1. Melhores restaurantes dos principais tipos culinários.
2. Top restaurantes mais bem avaliados e suas principais informações.
3. Top 10 melhores tipos de culinária, em termos de avaliação.
4. Top 10 piores tipos de culinária, em termos de avaliação.

# 4. Top 3 insights de dados

1. Apesar do país Indonésia ter poucos restaurantes cadastrados, em comparação aos outros países, possui a maior quantidade média de avaliações registradas.
2. Apesar da cidade de São Paulo ser uma das top 10 cidades com mais tipos distintos de culinária ela também está nas top 7 cidades com média de avaliação abaixo de 2,5.
3. Considerando todos os países e todas as culinárias cadastradas na plataforma, a culinária do tipo Ramen está no top 10 melhores culinárias e o tipo brasileira está no top 10 piores culinárias, em termos de avaliações.

# 5. O produto final do projeto

Dashboard online, hospedado em Cloud e disponível para acesso através de qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: 

[Main Page](https://aruacd-projects-fome-zero.streamlit.app/)

# 6. Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e tabelas em um dashboard interativo com o intuito de exibir as principais métricas de negócio da empresa da melhor forma possível para auxiliar na tomada de decisões por parte do CEO.

# 7. Próximos passos

1. Inserir diferentes tipos de gráficos no dashboard.
2. Criar outros tipos de filtros.
3. Adicionar novas visões de negócio.
