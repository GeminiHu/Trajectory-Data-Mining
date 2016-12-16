import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math as m
from math import radians, cos, sin, asin, sqrt 
import xlrd
import time

#¶ÁÈ¡µÀÂ·ÍøÂç
with open('E://WSC225//GPS//GpsData//zigong.pickle', 'rb') as f_pickle:
    zigong = pickle.load(f_pickle)
f_pickle.close() 
zg_mmap = zigong[6]
zg_mnx = zigong[5]
zg_nx = zigong[3]
zg_map = zigong[2]
position = zigong[4]
grid_map = zigong[7]
position = zigong[4]
with open('E://WSC225//GPS//GpsData//local_map.pickle', 'rb') as f_pickle:
    local_map = pickle.load(f_pickle)
f_pickle.close() 

sta = []
for i in xrange(138):
    for j in xrange(267):
        C_nx = nx.Graph() 
        if len(local_map[i][j]['ID']) > 150:
            sta.append(len(local_map[i][j]['ID']))
            for index in xrange(len(local_map[i][j]['s.id'])):
                C_nx.add_weighted_edges_from([(local_map[i][j]['s.id'][index],local_map[i][j]['e.id'][index],local_map[i][j]['distance'][index])]) 
            C_nx.remove_node(0)
            nx.draw(C_nx,position,with_labels = True,node_size = 10,width = 1)  
            plt.show()
print ''
#sta = []
#for i in xrange(138):
    #sta.append([])
    #for j in xrange(267):
        #if len(grid_map[i][j]['s.id']) > 1:
            ##C_nx = nx.Graph() 
            #for index in xrange(len(grid_map[i][j]['s.id'])):
                #sta[i].append((grid_map[i][j]['way.id'][index],grid_map[i][j]['segment.id'][index]))
                ##C_nx.add_weighted_edges_from([(grid_map[i][j]['s.id'][index],grid_map[i][j]['e.id'][index],grid_map[i][j]['distance'][index])])
            ##C_nx.remove_node(0)
            ##nx.draw(C_nx,position,with_labels = True,node_size = 10,width = 1)                   
            ##plt.show()
#plt.plot([(len(set(sta[i-1]))+len(set(sta[i]))+len(set(sta[i+1])))/3 for i in xrange(1,len(sta)-1)],'*')
#plt.show()