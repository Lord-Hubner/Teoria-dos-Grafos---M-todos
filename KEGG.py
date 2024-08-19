import urllib.request
import ssl
import re

stri = "http://rest.kegg.jp/%s/%s"
url = stri % ("list", "organism")

context = ssl._create_unverified_context()
# with urllib.request.urlopen(url, context=context) as response:
#     data = response.read().decode('utf-8')

# If you need the data as a string, decode it:

# print(data)

#Flavobacterium psychrophilum FPG3 - fpo

url = stri % ('find', 'enzyme') +'/fpo'

with urllib.request.urlopen(url, context=context) as response:
    data = response.read().decode('utf-8')

print(data)


listEnzymes = list()
listEnzymesNames = list()
n=0

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

print(listReactions)

listCompounds = list()

numReac = len(listReactionCodes)
for reaction in listReactionCodes:
    url = f'https://rest.kegg.jp/link/compound/{reaction}'
    with urllib.request.urlopen(url, context=context) as response:
        data = response.read().decode('utf-8')

    matches = re.findall(r'C\d{5}', data)
    for match in matches:
        listCompounds.append(match)

    open('Compostos', 'w')

    if listCompounds:
        with open('Compostos', 'a') as fp:
            fp.write(f'{reaction}: ')
            for comp in listCompounds:
                fp.write(f'{comp},')
            fp.write('\n')


idsSet = set()
with open('Compostos', 'r') as file:
    idsSet.update(file.readline())
ids_compounds = {k: index for index, k in enumerate(idsSet)}

print(data)



