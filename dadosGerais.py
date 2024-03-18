import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

#le a tabela base de clientes, usa tab como separador e exclui as linhas em branco
baseCliente = pd.read_csv('./baseClientes.csv', sep='\t', skip_blank_lines=True)

#remove cpfs duplicados da base de clientes
baseClienteUnicos = baseCliente.drop_duplicates(subset=['cpf'])  

#le a tabela base de transacoes, usa ; como separador, exclui as linhas em branco
baseTransacoes = pd.read_csv('./baseTransacoes.csv', sep=';', skip_blank_lines=True)

#exclui a última coluna que estava em branco 
baseTransacoes = baseTransacoes.drop(columns=['Unnamed: 6'])

#converte a coluna para data, pois o formato não era o ideal
baseTransacoes['data'] = pd.to_datetime(baseTransacoes['data'], format='%b-%y')

#formatei os dados da coluna para que mantivesse o formato de mes e ano, como usamos no br
baseTransacoes['data'] = baseTransacoes['data'].dt.strftime('%m/%Y')

#junta as tabelas usando o cpf como key(primary key e foreigner key)
tabelaCruzadas = pd.merge(baseClienteUnicos, baseTransacoes, on="cpf")

#deixa os nomes dos estabelecimentos todos em caixa baixa
tabelaCruzadas['estabelecimento'] = tabelaCruzadas['estabelecimento'].str.lower()

#padronizar os nomes das lojas, no caso apenas a zara que tinha variaçoes 
tabelaCruzadas['estabelecimento'] = tabelaCruzadas['estabelecimento'].replace({'zara ibirap': 'zara', 'zara analia fr': 'zara', 'zara morumbi': 'zara','zara plazasul': 'zara'})

#busca por cpfs unicos na tabela
totalClientes = tabelaCruzadas['cpf'].nunique()
print("O número total de clientes com Cpf's únicos, são:", totalClientes)

#salvar nova tabela
#caminho = 'tabelaCruzadas.csv'
#tabelaCruzadas.to_csv(caminho, index=False)
