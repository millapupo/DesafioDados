import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

tabelaCruzadas = pd.read_csv('./tabelaCruzadas.csv')

#le a tabela base de clientes, usa tab como separador e exclui as linhas em branco
baseCliente = pd.read_csv('./baseClientes.csv', sep='\t', skip_blank_lines=True)

#remove cpfs duplicados da base de clientes
baseClienteUnicos = baseCliente.drop_duplicates(subset=['cpf'])  

#definicao das faixas etarias para conseguir saber o perfil etario da base
faixasEtarias = [(0, 17), (18, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 84), (85, 120)]
nomesFaixas = ['0-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75-84', '85+']
baseClienteUnicos['idade'] = pd.cut(baseClienteUnicos['idade'], bins=[idade[0] for idade in faixasEtarias] + [120], labels=nomesFaixas)
faixaEtariaCount = baseClienteUnicos['idade'].value_counts().sort_index()
print(faixaEtariaCount)

totalClientes = faixaEtariaCount.sum()
porcentagemEtaria = round((faixaEtariaCount / totalClientes) * 100)

print("Distribuição percentual de faixa etária:")
print(porcentagemEtaria)

df_porcentagem = pd.DataFrame({'Faixa Etária': nomesFaixas, 'Porcentagem': porcentagemEtaria})
#grafico
plt.figure(figsize=(10, 6))
bars = plt.bar(df_porcentagem['Faixa Etária'], df_porcentagem['Porcentagem'], color='skyblue')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.3, f'{yval}%', ha='center', va='bottom')
plt.xlabel('Faixa Etária')
plt.ylabel('Porcentagem (%)')
plt.title('Distribuição Percentual de Faixa Etária')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

clientesPorEstado = baseClienteUnicos['estado'].value_counts()

print("Dados demográficos dos clientes, quantos clientes por estado:")
print(clientesPorEstado)

#grafico
plt.figure(figsize=(10, 6))
bars = clientesPorEstado.plot(kind='bar', color='skyblue')
plt.xlabel('Estado')
plt.ylabel('Número de Clientes')
plt.title('Número de Clientes por Estado')
plt.xticks(rotation=0)  
for bar in bars.patches:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, round(yval), ha='center', va='bottom')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

mediaGastosPorEstado = tabelaCruzadas.groupby('estado')['valor'].mean()
mediaGastosPorEstado = mediaGastosPorEstado.sort_values(ascending=False)
print("Média de gasto por estado:")
print(mediaGastosPorEstado)

mediaGastosPorEstado = {
    'TO': 309.268293,
    'MS': 307.124711,
    'RJ': 305.390374,
    'PR': 304.837037,
    'SP': 300.065524,
    'MG': 295.737685,
    'RS': 257.865385
}
#ordena
mediaGastosPorEstado = sorted(mediaGastosPorEstado.items(), key=lambda x: x[1], reverse=True)
estados, medias = zip(*mediaGastosPorEstado)

#grafico
plt.figure(figsize=(10, 6))
bars = plt.bar(estados, medias, color='skyblue')
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, f'{yval:.2f}', ha='center', va='bottom')
plt.xlabel('Estado')
plt.ylabel('Média de vendas ($)')
plt.title('Média de Vendas por Estado')
plt.xticks(rotation=0)  # Rotaciona os rótulos do eixo x para melhor visualização
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

vendasPorEstado = tabelaCruzadas.groupby(['estado','estabelecimento'])['valor'].sum()
maiorVendaPorEstado = {}
for estado in vendasPorEstado.index.levels[0]:
    vendasEstado = vendasPorEstado.loc[estado]
    estabelecimentoMaiorVenda = vendasEstado.idxmax()
    maiorVenda = vendasEstado.max()
    maiorVendaPorEstado[estado] = (estabelecimentoMaiorVenda,maiorVenda)

print("Estabelecimentos com maior venda em casa estado:")
for estado,(estabelecimento, valor) in maiorVendaPorEstado.items():
    print(f"Estado: {estado}| Estabelecimento: {estabelecimento}| Valor: {valor}")