from math import cos, sin, pi
from matplotlib import pyplot as plt
from random import random

def plot_graph(M, R=1., tk=2., labels=[]):
    N = len(M)
    dphi = 2*pi/N
    # nodes
    Xs = []
    Ys = []
    for ii in range(N):
        phi = ii*dphi
        Xs.append(R*cos(phi))
        Ys.append(R*sin(phi))
    # links
    links = []
    for ii, line in enumerate(M):
        for jj, ele in enumerate(line):
            if ele:
                links.append( ( [Xs[ii], Xs[jj]], [Ys[ii], Ys[jj]] ) )
    # plots
    for link in links:
        plt.plot(link[0], link[1], color="black", linewidth=tk) #links
    plt.plot(Xs, Ys, 'ro') #nodes
    if labels:
        for ii in range(N):
            plt.text(Xs[ii], Ys[ii], labels[ii], color="green", size=30)
    plt.axis([-R*1.2, R*1.2, -R*1.2, R*1.2])
    plt.show()

def clustering(M):
    N = len(M)
    Cs = [0 for ii in range(N)]
    for ii, line in enumerate(M):
        ki = sum(line)
        if ki>1:
            neigs = [jj for jj in range(N) if line[jj] ]
            Ei = .5*sum([ M[jj][kk]>=1 for jj in neigs for kk in neigs])
            Cs[ii] = 2*Ei/(ki*(ki-1))
    return Cs


def stats(lista):
    N = len(lista)
    xb = sum(lista)*1./N
    if N>1:
        var = sum([(xb-ele)**2 for ele in lista])*1./(N-1)
    else:
        var = 0
    return xb, var**.5


def correlation(lista1, lista2):
    x1, s1 = stats(lista1)
    x2, s2 = stats(lista2)
    N = len(lista1)
    corr = sum([(lista1[ii]-x1)*(lista2[ii]-x2) for ii in range(N)])/((N-1)*s1*s2)
    return corr

def assort(M):
    N = len(M)
    kis = [sum(ele) for ele in M]
    kbs = []
    for kk, ki in enumerate(kis):
        neigbs = [ii for ii in range(N) if M[kk][ii]]
        kbns = [kis[ii] for ii in neigbs]
        if kbns:
            kbs.append(stats(kbns)[0])
        else:
            kbs.append(0.)
    a = plt.axis([min(kis)-1, max(kis)+1, min(kbs)-1, max(kbs)+1])
    a = plt.plot(kis, kbs, 'bo')
    plt.show()
    return correlation(kis, kbs)


def rand_graph(N, p):
    M = [[0 for ii in range(N)] for jj in range(N)]
    for ii in range(N):
        for jj in range(ii+1, N):
            if random()<p:
                M[ii][jj] = 1
                M[jj][ii] = 1
    return M



if 0:
    M = [[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]]
    ks = [sum(linea) for linea in M]
    N = len(M)
    labels = [chr(ele) for ele in range(65, 65+N)]
    for ii in range(N):
        print("Node %s has degree %i"%(labels[ii], ks[ii]))
    Cs = clustering(M)
    print(sum(Cs)/N)
    a = assort(M)


if 0:
    p = .01
    N = 1000
    M = rand_graph(N, p)
    plot_graph(M, R=100., tk=.1)
    kis = [sum(ele) for ele in M]
    nlinks = sum(kis)/2
    cs = clustering(M)
    ass = assort(M)
    print("Links expected: %f. Links obtained: %i"%(p*N*(N-1)/2, nlinks))
    print("cbar=%f assort=%f kb=%f"%(sum(cs)/1000, ass, sum(kis)/1000.))
    a = plt.hist(kis)
    plt.show()



from urllib.request import urlopen

stri = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"

www = urlopen(stri)
data = www.readlines()

data = [ele.decode().split(",") for ele in data]
N = len(data)
inis = [ele[2] for ele in data]
fins = [ele[4] for ele in data]

airps = list(set(inis+fins))
Na = len(airps)
M = [[0 for ii in range(Na)] for jj in range(Na)]

for ii in range(N):
    airpi = inis[ii]
    airpf = fins[ii]
    INIair = airps.index(airpi)
    FINair = airps.index(airpf)
    M[INIair][FINair] = 1
    M[FINair][INIair] = 1

kis = [sum(ele) for ele in M]
cs = clustering(M)
print(sum(cs)/Na)
ass = assort(M)
a = plt.hist(kis, max(kis))
plt.show()



# import json

# apikey = "" # cada um coloca sua chave aqui
# stri = "http://iatacodes.org/api/v6/airports?api_key=%s&code=%s"

# www = urlopen(stri%(apikey, "POA"))
# data = www.read()
# jdata = json.loads(data)
# jdata["response"][0]["name"]

# kis = [sum(ele) for ele in M]
# im = kis.index(max(kis))

# www = urllib2.urlopen(stri%(apikey, airps[im]))
# data = www.read()
# jdata = json.loads(data)
# jdata["response"][0]["name"]

# for code in airps:
#     www = urllib2.urlopen(stri%(apikey, code))
#     data = www.read()
#     jdata = json.loads(data)
#     if jdata["response"]:
#         name = jdata["response"][0]["name"]
#         #country = jdata["response"][0]["country_code"]
#         print(code, name)  #, country
#     else:
#         print(" --> No answer for %s"%code)





# ######## small world

# def walk(nodei, distances, neigbs, N, not_visited, distance):
#     while not_visited:
#         distance +=1
#         for nodej in neigbs[nodei]:
#             if distances[nodej] > distance:
#                 distances[nodej] = distance
#         # Prepares next step
#         togo = [distances[ii] for ii in not_visited]
#         next = not_visited[togo.index(min(togo))]
#         next = not_visited.pop(not_visited.index(next))
#         distance = distances[next]
#         if distance>=N:
#             return None
#         walk(next, distances, neigbs, N, not_visited, distance)

# from time import time

# def calc_distances(neigbs, nodei):
#     ti = time()
#     N = len(neigbs)
#     not_visited = range(N)
#     distances = [N+1 for ii in range(N)]
#     distances[nodei] = 0
#     distance = 0
#     not_visited.pop(nodei)
#     walk(nodei, distances, neigbs, N, not_visited, distance)
#     tf = time()
#     print("No %i in %f s"%(nodei, tf-ti))
#     return distances


# def calc_all_distances(M):
#     N = len(M)
#     neigbs = [[ii for ii, ele in enumerate(line) if ele] for line in M]
#     dist_matrix = [calc_distances(neigbs, ii) for ii in range(N)]
#     return dist_matrix







