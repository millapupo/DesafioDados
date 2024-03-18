import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tabelaCruzadas = pd.read_csv('./tabelaCruzadas.csv')
#le a tabela base de clientes, usa tab como separador e exclui as linhas em branco
baseCliente = pd.read_csv('./baseClientes.csv', sep='\t', skip_blank_lines=True)

#remove cpfs duplicados da base de clientes
baseClienteUnicos = baseCliente.drop_duplicates(subset=['cpf'])  

#para saber a quantidade e % de clientes por gênero
totalClientePorGenero = baseClienteUnicos['sexo'].value_counts()
totalClientes = totalClientePorGenero.sum()
numeroMulheres = totalClientePorGenero['feminino']
numeroHomens = totalClientePorGenero['masculino']
cliMulheres = round((totalClientePorGenero['feminino']/totalClientes)*100)
cliHomens = round((totalClientePorGenero['masculino']/totalClientes)*100)

print("Número de clientes por gênero:")
print(totalClientes)
#grafico
plt.figure(figsize=(8, 8))
labels = ['Mulheres', 'Homens']
sizes = [cliMulheres, cliHomens]
colors = ['lightcoral', 'lightskyblue']
explode = (0.1, 0)  # Explode a primeira fatia (Mulheres)

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Distribuição de Clientes por Gênero')
plt.axis('equal')  
plt.tight_layout()
plt.show()

print(f"Mulheres: {numeroMulheres} ({cliMulheres}%)")
print(f"Homens: {numeroHomens}({cliHomens}%)")

#algumas diferenças no comportamento de compras por gênero, listando o total de gastos        
vendasPorGenero = tabelaCruzadas.groupby('sexo')['valor'].sum()
print("\nVendas por gênero")
print(vendasPorGenero)

#fiz media e mediana para ver se tinha alguma discrepancia muito grande nos dados, mas não notei nada absurdo
vendasMediaPorGenero = tabelaCruzadas.groupby('sexo')['valor'].mean()
vendasMedianaPorGenero = tabelaCruzadas.groupby('sexo')['valor'].median()

#relacionei os dados dos gastos x a renda e criei uma nova coluna com a porcentagem dos gastos
tabelaCruzadas['porcentagemGastos'] = ((tabelaCruzadas['valor'] / tabelaCruzadas['renda']) *100)
tabelaCruzadas['porcentagemGastos'] = tabelaCruzadas['porcentagemGastos'].apply(lambda x: f"{x:.2f}")

#separar gastos, genero e estabelecimentos
vendasPorGeneroEstabelecimentos = tabelaCruzadas.groupby(['sexo', 'estabelecimento'])['valor'].sum()

#gastos por gêneros
gastosMulheres = vendasPorGeneroEstabelecimentos.loc['feminino']
gastosHomens = vendasPorGeneroEstabelecimentos.loc['masculino']

#loja mais consumida por gênero 
maisConsumidaMulheres = gastosMulheres.idxmax()
maisConsumidaHomens = gastosHomens.idxmax()

#loja menos consumida por gênero 
menosConsumidaMulheres = gastosMulheres.idxmin()
menosConsumidaHomens = gastosHomens.idxmin()
""
print("Loja mais consumida por mulheres:", maisConsumidaMulheres)
print("Loja menos consumida por mulheres:", menosConsumidaMulheres)
print("Loja mais consumida por homens:", maisConsumidaHomens)
print("Loja menos consumida por homens:", menosConsumidaHomens)

topLojasMulheres = gastosMulheres.nlargest(5)
topLojasHomens = gastosHomens.nlargest(5)

print("\nTop 5 lojas mais consumidas por mulheres:")
print(topLojasMulheres)
print("\nTop 5 lojas mais consumidas por homens:")
print(topLojasHomens)