#本程序实现基于nodes表与network表的可视化
import xlrd
import xlwt
from xlutils.copy import copy
import networkx as nx
import matplotlib.pyplot as plt
import pickle

#网络的可视化
nodes = 'real_test_nodes.xlsx'
network = 'real_test_network.xlsx'
#打开test的数据表格
t_network = xlrd.open_workbook('E://WSC225//GPS//GpsData//'+network)
tnx = t_network.sheets()[0]
t_nodes = xlrd.open_workbook('E://WSC225//GPS//GpsData//'+nodes)
tnd = t_nodes.sheets()[0]
#建立网络
G_T = nx.Graph()   #建立以时间为权重的空无向图
G_T.position = {}  #G_T的节点定位
nr = tnx.nrows
for i in xrange(nr-1):
    sp = int(tnx.cell(i+1,0).value)
    ep = int(tnx.cell(i+1,1).value)
    at = 1
    G_T.add_weighted_edges_from([(sp,ep,at)])
    G_T.position[sp] = (tnd.cell(sp,1).value*10**6-104000000,tnd.cell(sp,2).value*10**6-104000000)
    G_T.position[ep] = (tnd.cell(ep,1).value*10**6-104000000,tnd.cell(ep,2).value*10**6-104000000)
nx.draw(G_T,G_T.position,with_labels=True,node_size = 200,width = 5)                   #绘制网络G_T
plt.show()