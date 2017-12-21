#!/usr/bin/env python
import networkx as nx
from matplotlib import pyplot as plt
import math
import csv
import random as rand
import sys

_DEBUG_ = False

#this method just reads the graph structure from the file
def buildG(G, file_, delimiter_):
    #construct the weighted version of the contact graph from cgraph.dat file
    #reader = csv.reader(open("/home/kazem/Data/UCI/karate.txt"), delimiter=" ")
    reader = csv.reader(open(file_), delimiter=delimiter_)
    for line in reader:
        if len(line) > 2:
            if float(line[2]) != 0.0:
                #line format: u,v,w
                G.add_edge(int(line[0]),int(line[1]),weight=float(line[2]))
        else:
            #line format: u,v
            G.add_edge(int(line[0]),int(line[1]),weight=1.0)

#keep removing edges from Graph until one of the connected components of Graph splits into two
#compute the edge betweenness
def CmtyGirvanNewmanStep(G):
    if _DEBUG_:
        print "Calling CmtyGirvanNewmanStep"
    init_ncomp = nx.number_connected_components(G)    #no of components
    ncomp = init_ncomp
    while ncomp <= init_ncomp:
        bw = nx.edge_betweenness_centrality(G, weight='weight')    #edge betweenness for G
        #find the edge with max centrality
        max_ = max(bw.values())
        #find the edge with the highest centrality and remove all of them if there is more than one!
        for k, v in bw.iteritems():
            if float(v) == max_:
                G.remove_edge(k[0],k[1])    #remove the central edge
        ncomp = nx.number_connected_components(G)    #recalculate the no of components

#compute the modularity of current split
def _GirvanNewmanGetModularity(G, deg_, m_):
    New_A = nx.adj_matrix(G)
    New_deg = {}
    New_deg = UpdateDeg(New_A, G.nodes())
    #Let's compute the Q
    comps = nx.connected_components(G)    #list of components    
    print 'No of communities in decomposed G: %d' % nx.number_connected_components(G)
    Mod = 0    #Modularity of a given partitionning
    for c in comps:
        EWC = 0    #no of edges within a community
        RE = 0    #no of random edges
        for u in c:
            EWC += New_deg[u]
            RE += deg_[u]        #count the probability of a random edge
        Mod += ( float(EWC) - float(RE*RE)/float(2*m_) )
    Mod = Mod/float(2*m_)
    if _DEBUG_:
        print "Modularity: %f" % Mod
    return Mod

def UpdateDeg(A, nodes):
    deg_dict = {}
    n = len(nodes)  #len(A) ---> some ppl get issues when trying len() on sparse matrixes!
    B = A.sum(axis = 1)
    for i in range(n):
        deg_dict[nodes[i]] = B[i, 0]
    return deg_dict

#run GirvanNewman algorithm and find the best community split by maximizing modularity measure
def runGirvanNewman(G, Orig_deg, m_):
    #let's find the best split of the graph
    BestQ = 0.0
    Q = 0.0
    while True:    
        CmtyGirvanNewmanStep(G)
        Q = _GirvanNewmanGetModularity(G, Orig_deg, m_);
        print "Modularity of decomposed G: %f" % Q
        if Q > BestQ:
            BestQ = Q
            BestG = nx.copy.deepcopy(G)    #Best G
#            for comp in nx.connected_components(G):
#                print comp
        if G.number_of_edges() == 0:
            break
    if BestQ > 0.0:
        print "Max modularity (Q): %f" % BestQ
    else:
        print "Max modularity (Q): %f" % BestQ

    return BestG

def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <input graph>\n" % (argv[0],))
        return 1
    G = runGNfromFile(argv[1])
    draw(G)

def runGNfromFile(filename):
    graph_fn = filename
    G = nx.Graph()  #let's create the graph first
    buildG(G, graph_fn, ',')
    
    if _DEBUG_:
        print 'G nodes:', G.nodes()
        print 'G no of nodes:', G.number_of_nodes()
    
    n = G.number_of_nodes()    #|V|
    A = nx.adj_matrix(G)    #adjacenct matrix

    m_ = 0.0    #the weighted version for number of edges
    for i in range(0,n):
        for j in range(0,n):
            m_ += A[i,j]
    m_ = m_/2.0
    if _DEBUG_:
        print "m: %f" % m_

    #calculate the weighted degree for each node
    Orig_deg = {}
    Orig_deg = UpdateDeg(A, G.nodes())

    #run Newman alg
    return runGirvanNewman(G, Orig_deg, m_)

def draw(G):
    pos = nx.spring_layout(G)
    pos = nx.spring_layout(G, pos=pos)
    pos = nx.spring_layout(G, pos=pos)
    pos = nx.spring_layout(G, pos=pos)
    pos = nx.spring_layout(G, pos=pos)
    pos = nx.spring_layout(G, pos=pos)
    
    nodeLabelDict = {}
    for node in G.nodes():
        nodeLabelDict[node] = '{node}'.format(node=node)

    edgeLabelDict = {}
    for edge in G.edges():
        edgeLabelDict[edge] = '%.4f' % G.adj[edge[0]][edge[1]]['weight']

    nx.draw_networkx_nodes(G,pos,node_size=100, node_color="white")
    nx.draw_networkx_edges(G,pos, width=1,alpha=0.5,edge_color='black')
    nx.draw_networkx_labels(G,pos,labels=nodeLabelDict, font_size=10,font_family='sans-serif')
    nx.draw_networkx_edge_labels(G, pos, edgeLabelDict)

    plt.show()

    for comp in nx.connected_components(G):
        print comp

if __name__ == "__main__":
    sys.exit(main(sys.argv))
