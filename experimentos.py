from matplotlib import pyplot as plt

M=[[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0], [1,
 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1,
 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0,
 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0,
 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]]

ks = [sum(linea) for linea in M]
N =len(M)
labels = [chr(ele) for ele in range(65, 65+N)]

for ii in range(N):
    print('Node %s has degree %i' %(labels[ii], ks[ii]))





from math import cos, sin, pi
def plot_graph(M, R=1., tk=2., labels=[]):
    N =len(M)
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
        plt.plot(link[0], link[1], color='black' , linewidth=tk) #links
    plt.plot(Xs, Ys, 'ro') #nodes
    if labels:
        for ii in range(N):
            plt.text(Xs[ii], Ys[ii], labels[ii], color='green' , size=30)
    plt.axis([-R*1.2, R*1.2,-R*1.2, R*1.2])
    plt.show()  

plot_graph(M, labels=labels)