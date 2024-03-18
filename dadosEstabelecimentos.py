import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

tabelaCruzadas = pd.read_csv('./tabelaCruzadas.csv')

#busca por cpfs unicos na tabela
totalClientes = tabelaCruzadas['cpf'].nunique()
print("O número total de clientes com Cpf's únicos, são:", totalClientes)

#mostra a evolução de venda geral por mes
gastoMes = tabelaCruzadas.groupby('data')['valor'].sum()

#grafico
gastoMes.plot(kind='bar', figsize=(10,6))
plt.title('Evolução do gasto por mês')
plt.xlabel('Mês/Ano')
plt.ylabel('Valor gasto')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

print("Gastos total no mês:")
print(gastoMes)

vendasPorEstabelecimentos = tabelaCruzadas.groupby('estabelecimento')['valor'].sum()
#gráfico
labels = vendasPorEstabelecimentos.index  
valores = vendasPorEstabelecimentos.values  
plt.figure(figsize=(8, 8))  
plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140)  
plt.title('Distribuição de Vendas por Estabelecimento')  
plt.show()

#juntar por mês, establecimentos e somar o valor das vendas final
vendasPorMesesEstabelecimentos = tabelaCruzadas.groupby(['data','estabelecimento'])['valor'].sum()
print("Vendas no mês e por estabelecimento")
print(vendasPorMesesEstabelecimentos)

#buscar pelo establecimento com mais venda no mês
meses = vendasPorMesesEstabelecimentos.index.levels[0] #acessa os meses
maiorVendaPorMes = {} #cria um dicionário para armazenar os dados dos estabelecimentos
for mes in meses: #for para iterar os estabelecimentos e achar qual vendeu mais
    vendaMes = vendasPorMesesEstabelecimentos.loc[mes]
    estabelecimentoMaiorVenda = vendaMes.idxmax()
    maiorVenda = vendaMes.max()
    maiorVendaPorMes[mes] = (estabelecimentoMaiorVenda, maiorVenda)
  
print("\nEstabelecimento com maior venda no mês:")
for mes, (estabelecimento, valor) in maiorVendaPorMes.items():
        print(f"Data: {mes} | Estabelecimento: {estabelecimento} | Valor: {valor}")

evolucaoMesAMesEstabelecimentos = tabelaCruzadas.groupby(['data','estabelecimento'])['valor'].sum()

dfVendas = vendasPorMesesEstabelecimentos.unstack()
#grafico de linhas
plt.figure(figsize=(12, 6))  
for estabelecimento in dfVendas.columns:
    plt.plot(dfVendas.index, dfVendas[estabelecimento], label=estabelecimento)

plt.title('Crescimento de Vendas por Estabelecimento Mês a Mês')
plt.xlabel('Mês/Ano')
plt.ylabel('Valor de Vendas')
plt.xticks(rotation=45)
plt.legend(title='Estabelecimento', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()  