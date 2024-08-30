import urllib.request
import ssl
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from graph import plot_graph, clustering, stats, correlation, assort, rand_graph

pd.set_option("display.max.columns", None)


def SearchEnzymes(data, listEnzymes, listEnzymesNames, n):
    while True:
        index = data.find('\n', n)
        if index == -1:
            break
        thisEnzyme = data[n:index]
        match = re.match(r'^ec:\d{1}(\.\d+){3}', thisEnzyme)
        if (match):
            listEnzymes.append(thisEnzyme)
            listEnzymesNames.append(match.group(0))
        n=index+1
    return listEnzymes, listEnzymesNames


def SearchReactions(stri, context, listEnzymesNames):
    listReactions = list()
    listReactionCodes = list()
    for enzyme in listEnzymesNames:
        url = stri % ('link', 'reaction')+f'/{enzyme}'

        with urllib.request.urlopen(url, context=context) as response:
            data = response.read().decode('utf-8')

        index = data.find('R')
        match = re.match(r'R\d{5}', data[index:-1])
        if (match):
            listReactionCodes.append(match.group(0))   
            listReactions.append(data)
    return listReactions, listReactionCodes



stri = "http://rest.kegg.jp/%s/%s"
url = stri % ("list", "organism")

context = ssl._create_unverified_context()

# with urllib.request.urlopen(url, context=context) as response:
#     data = response.read().decode('utf-8')

# print(data)

#Flavobacterium psychrophilum FPG3 - fpo
#Ornithorhynchus anatinus (platypus) - oaa

url = stri % ('find', 'enzyme') +'/etf'

with urllib.request.urlopen(url, context=context) as response:
    data = response.read().decode('utf-8')

print(data)

listEnzymes = list()
listEnzymesNames = list()
n=0

listEnzymes, listEnzymesNames = SearchEnzymes(data, listEnzymes, listEnzymesNames, n)

listReactions, listReactionCodes = SearchReactions(stri, context, listEnzymesNames)  

print(listReactions)

def SearchCompounds(context, listReactionCodes, overwrite):
    
    reactionsCompounds = list()
    isFile = os.path.isfile("Compostos.txt")  
    if not overwrite and isFile:
        return
        
    open("Compostos.txt", 'w')
    for reaction in listReactionCodes:
        url = f'https://rest.kegg.jp/link/compound/{reaction}'
        with urllib.request.urlopen(url, context=context) as response:
            data = response.read().decode('utf-8')


        matches = re.findall(r'C\d{5}', data)
        reactionsCompounds.append(matches)
    
        if matches:
            with open('Compostos.txt', 'a') as fp:
                length = len(matches)
                fp.write(f'{reaction}: ')
                for index in range(length-1):
                    fp.write(f'{matches[index]},')
                fp.write(matches[index+1])              
                fp.write('\n')
    return reactionsCompounds

reactionsCompounds = list()
reactionsCompounds = SearchCompounds(context, listReactionCodes, True)

idsSet = set()
reactionsDict = dict()
counter = 0
with open('Compostos.txt', 'r') as file:
    while True:
        line = file.readline()
        if len(line) == 0:
            break           
        index = line.find(':')
        reactionCode = line[:index]  
        reactionsDict[counter] = reactionCode 
        line = line[index+2:].replace('\n','')      
        idsSet.update([code for code in line.split(',')])
        counter += 1

compoundsReactionsDict = dict()
for i in range(len(reactionsCompounds)):
    for compound in reactionsCompounds[i]:
        if not compoundsReactionsDict.get(compound):
            compoundsReactionsDict[compound] = [i]
        else:
            compoundsReactionsDict[compound].append(i)


# reactionsCompoundsDict = {k: index for reactionIndex, compounds in enumerate(reactionsCompounds)}
reactionNumber = len(listReactions)

matrix = list()

def GetDegree(compound1, compound2, compoundsReactionsDict):
    counter = 0
    for reactionCompound1 in compoundsReactionsDict[compound1]:
        for reactionCompound2 in compoundsReactionsDict[compound2]:
            if reactionCompound1 == reactionCompound2:
                counter += 1
    return counter

for i in idsSet:
    xthList = list()
    for j in idsSet:
        if i == j:
            xthList.append(0)
            continue
        currentDegree = GetDegree(i, j, compoundsReactionsDict)
        xthList.append(currentDegree)
    matrix.append(xthList)

compoundsList = [compound for compound in idsSet]

matrixFrame = pd.DataFrame(matrix, columns=compoundsList, index=compoundsList)
print(matrixFrame)

matrixFrame.to_csv('CompoundsMatrix.csv')

#Estatísticas
nVertices = len(idsSet)

print('\nEstatísticas da rede metabólica:\n')
kis = [sum(lin) for lin in matrix]
nlinks = sum(kis) / 2
cs = clustering(matrix)         # Calcula o coeficiente de clustering local para cada nó
mcs = sum(cs) / nVertices         # Calcula o coeficiente de clustering médio da rede
ass = assort(matrix)     # Calcula a assortatividade e plota o gráfico de dispersão desta
# Coef. de clustering do grafo corresponde a média dos coef. de clustering local de cada vértice
print(f'Coeficiente de clustering global: {mcs}')
print(f'Assortatividade: {ass}')
print(f'Links (arestas) totais: {nlinks}')

plot_graph(matrix)
# print(f"Clustering: {clustering(matrix)}")
# print(f"Stats: {stats(matrix)}")
# print(f"Correlation")

plt.cla()

# Histograma dos graus da rede metabólicas
metNetwork, metLen = kis, len(set(kis))
plt.hist(metNetwork, color='blue')
plt.ylabel('Número de nós')
plt.xlabel('Grau')
plt.title('Distribuição dos graus dos nós na rede metabólica')
# plt.yscale('symlog') # Põe o eixo y em escala logarítmica, pois alguns nós tem grau muito elevado
plt.show()



print('\nEstatísticas da rede aleatória:\n')
matriz = rand_graph(nVertices, 0.642)
kisx = [sum(lin) for lin in matriz]
nlinksx = sum(kisx) / 2
csx = clustering(matriz)  # Demorou alguns minutos para calcular o clustering da rede aleatória       
mcsx = sum(csx) / nVertices        
assx = assort(matriz)
print(f'Coeficiente de clustering global: {mcsx}')
print(f'Assortatividade: {assx}')
print(f'Links (arestas) totais: {nlinksx}')

plt.cla()

plot_graph(matriz)

# Histograma dos graus da rede aleatória
aleNetwork, aleLen = kisx, len(set(kisx))
plt.hist(aleNetwork, color='lightblue')
plt.ylabel('Número de nós')
plt.xlabel('Grau')
plt.title('Distribuição dos graus dos nós na rede aleatória')
# plt.yscale('symlog') # Põe o eixo y em escala logarítmica, pois alguns nós tem grau muito elevado
plt.show()


print("bah")





