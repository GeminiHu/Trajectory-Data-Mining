#本程序实现IVMM算法

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math as m
from math import radians, cos, sin, asin, sqrt 

#读取道路网络
with open('E://WSC225//GPS//GpsData//zigong.pickle', 'rb') as f_pickle:
    zigong = pickle.load(f_pickle)
f_pickle.close() 
#Candidates Preparation
zg_mmap = zigong[6]
zg_mnx = zigong[5]
position = zigong[4]

#N函数(待修改)
def N(x):
    #p = 1/std*m.sqrt(2*m.pi)
    #q = -((x-mean)**2)/(2*std**2)
    #return p*m.exp(q)
    return 1

#为得分矩阵加入权重
def f(x):
    beta = 30.0
    return beta/x #因指数权重太小，简化成反比例函数

#地球两点距离
def haversine(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """  
    # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r * 1000 #结果单位为米

#输入采样点与候选边，返回距离与候选点
def Candinate(t_lon,t_lat,s_lon,s_lat,e_lon,e_lat):
    st = haversine(t_lon,t_lat,s_lon,s_lat)
    te = haversine(t_lon,t_lat,e_lon,e_lat)
    se = haversine(e_lon,e_lat,s_lon,s_lat)
    flag = (st**2+se**2-te**2)/(2*se**2)
    if flag <= 0:
        return {'dis':st,'lon':s_lon,'lat':s_lat}
    elif flag >= 1:
        return {'dis':te,'lon':e_lon,'lat':e_lat}
    else:
        return {'dis':m.sqrt(st**2-(flag*se)**2),
                'lon':flag*(e_lon-s_lon)+s_lon,
                'lat':flag*(e_lat-s_lat)+s_lat}

def IVMM (trajectory,r):
    """ 
    trajectory存储路径的字典，r候选路径的选择范围（单位米）
    """  
    n_tra = len(trajectory['lon']) #采样点个数
    #确定CPS、CP
    C = []
    for i in xrange(n_tra):
        C.append({'CPS':[],'CP':[]})
        rank = [] #记录第i个采样点前五个最近候选点的距离
        min_lon = trajectory['lon'][i]-0.01
        max_lon = trajectory['lon'][i]+0.01
        min_lat = trajectory['lat'][i]-0.01
        max_lat = trajectory['lat'][i]+0.01
        for j in xrange(len(zg_mmap['s.id'])):
            dis_term = (zg_mmap['distance'][j]>900)
            slon_term = (zg_mmap['s.lon'][j]<max_lon and zg_mmap['s.lon'][j]>min_lon)
            slat_term = (zg_mmap['s.lat'][j]<max_lat and zg_mmap['s.lat'][j]>min_lat)
            elon_term = (zg_mmap['e.lon'][j]<max_lon and zg_mmap['e.lon'][j]>min_lon)
            elat_term = (zg_mmap['e.lat'][j]<max_lat and zg_mmap['e.lat'][j]>min_lat)
            if dis_term or (slon_term and slat_term and elon_term and elat_term):
                temp = Candinate(trajectory['lon'][i], trajectory['lat'][i], zg_mmap['s.lon'][j], zg_mmap['s.lat'][j], zg_mmap['e.lon'][j],zg_mmap['e.lat'][j])
                if temp['dis'] < 100:
                    if len(C[i]['CPS']) < 5:#限制候选路段数量
                        C[i]['CPS'].append((j,temp['dis']))
                        C[i]['CP'].append((temp['lon'],temp['lat']))
                        rank.append(temp['dis'])
                    else:
                        if temp['dis'] < max(rank):
                            for n in xrange(5):
                                if C[i]['CPS'][n][1] == max(rank):
                                    C[i]['CPS'].remove(C[i]['CPS'][n])
                                    C[i]['CP'].remove(C[i]['CP'][n])
                                    rank.remove(max(rank))
                                    C[i]['CPS'].append((j,temp['dis'])) #j是候选边在C_mmap中的index
                                    C[i]['CP'].append((temp['lon'],temp['lat']))
                                    rank.append(temp['dis'])
                                    break
    #每个采样点的候选点个数
    num_C = [0]*n_tra
    for i in xrange(n_tra):
        num_C[i] = len(C[i]['CP'])        
    #测试某条边的是哪一个采样点的候选边
    #for i in xrange(n_tra):
        #for k in xrange(num_C[i]):
            #index = C[i]['CPS'][k][0]
            #if  zg_mmap['s.id'][index]==3541169642 and zg_mmap['e.id'][index]==3540396699:
                #print 'i=',i,'k=',k
            #if  zg_mmap['e.id'][index]==3541169642 and zg_mmap['s.id'][index]==3540396699:
                #print 'i=',i,'k=',k
    #建立候选图
    C_nx = nx.Graph() 
    for sample_index in xrange(n_tra):
        for CPS_index in xrange(len(C[sample_index]['CPS'])):
            index = C[sample_index]['CPS'][CPS_index][0]
            C_nx.add_weighted_edges_from([(zg_mmap['s.id'][index],zg_mmap['e.id'][index],zg_mmap['distance'][index])])
    C_nx = max(nx.connected_component_subgraphs(C_nx), key=len)
    test_track = {'lon':[104.764204,104.764513,104.764398,104.764694,104.765473,104.765923,104.766667,104.766805],
                  'lat':[ 29.350574, 29.350602, 29.350958, 29.351147, 29.351463, 29.351486, 29.351478, 29.350898]}  
    for i in xrange(n_tra):
        C_nx.add_node(i,color = 'g',size = 300)
        position[i] = (test_track['lon'][i],test_track['lat'][i])
    #nx.draw(C_nx,position,with_labels = True,node_size = 10,width = 1)                   
    #plt.show()
    allpath = nx.shortest_path(C_nx)
    #任意两点距离
    D = np.zeros((n_tra,n_tra))
    for i in xrange(n_tra):
        for j in xrange(n_tra):
            D[i][j] = haversine(trajectory['lon'][i],trajectory['lat'][i],trajectory['lon'][j],trajectory['lat'][j])
            D[j][i] = D[i][j]
    #相邻采样点的候选点距离与最短路径
    d = [0]*(n_tra-1)
    w = [0]*(n_tra-1)
    for i in xrange(n_tra-1):
        d[i] = D[i][i+1]
        w[i] = np.zeros((num_C[i],num_C[i+1]))
        for j in xrange(num_C[i]):
            for k in xrange(num_C[i+1]):
                s_index = C[i]['CPS'][j][0]
                t_index = C[i+1]['CPS'][k][0]
                #path = nx.shortest_path(zg_mnx,source = zg_mmap['s.id'][s_index] ,target = zg_mmap['s.id'][t_index])
                try:
                    #path = nx.shortest_path(C_nx,source = zg_mmap['s.id'][s_index] ,target = zg_mmap['s.id'][t_index])
                    path = allpath[zg_mmap['s.id'][s_index]][zg_mmap['s.id'][t_index]]
                    #测试经过交叉节点的路径
                    #if 3540396699 in path:
                        #print #############################################
                        #print i,j,i+1,k
                        #print path,zg_mmap['s.id'][s_index],zg_mmap['s.id'][t_index]
                    #使造成回头路的节点前一个节点到达它的w为inf
                    #if i==0:
                        #####
                    #if i==1:
                        #####
                    #if i>=2:
                        #####
                except:
                    w[i][j][k] = float('inf')
                    continue
                if len(path) == 1:
                    w[i][j][k] = haversine(C[i]['CP'][j][0],C[i]['CP'][j][1],C[i+1]['CP'][k][0],C[i+1]['CP'][k][1])
                else:
                    if path[1] == zg_mmap['s.id'][s_index]:
                        delta1 = -haversine(C[i]['CP'][j][0],C[i]['CP'][j][1],zg_mmap['s.lon'][s_index],zg_mmap['s.lat'][s_index])
                    else:
                        delta1 = haversine(C[i]['CP'][j][0],C[i]['CP'][j][1],zg_mmap['s.lon'][s_index],zg_mmap['s.lat'][s_index])
                    if path[len(path)-2] == zg_mmap['e.id'][t_index]:
                        delta2 = -haversine(C[i+1]['CP'][k][0],C[i+1]['CP'][k][1],zg_mmap['s.lon'][t_index],zg_mmap['s.lat'][t_index])
                    else:
                        delta2 = haversine(C[i+1]['CP'][k][0],C[i+1]['CP'][k][1],zg_mmap['s.lon'][t_index],zg_mmap['s.lat'][t_index])
                    length = 0
                    for t in xrange(len(path)-1): 
                        length += zg_mnx.get_edge_data(path[t],path[t+1])['weight']
                    w[i][j][k] = delta1+delta2+ length
                #if w[i][j][k] <= 0:
                    ##print C[i]['CP']
                    ##print C[i+1]['CP']
                    ##print j
                    #print delta1,delta2,length,zg_mmap['s.id'][s_index],zg_mmap['s.id'][t_index]
                    #print C[i+1]['CP'][k][0],C[i+1]['CP'][k][1],C[i]['CP'][j][0],C[i]['CP'][j][1]
                    #print '******************************'
    #建立静态投票矩阵
    M = [0]*(n_tra-1)
    for i in xrange(n_tra-1):
        M[i] = np.zeros((num_C[i],num_C[i+1]))
        for j in xrange(num_C[i]):
            for k in xrange(num_C[i+1]):
                if w[i][j][k] != 0:
                    M[i][j][k] = N(C[i]['CPS'][j][1])*(d[i]/w[i][j][k])
                else:
                    M[i][j][k] = N(C[i]['CPS'][j][1])*(d[i]/5)
                #M[i][j][k] = d[i]/w[i][j][k]
                #if M[i][j][k] == float('inf') or M[i][j][k] < 0:
                    #print i,j,k
                    #print d[i]
                    #print w[i][j][k]
                    #print '******************************'
    phi = [0]*n_tra
    #for i in xrange(n_tra):
        #phi[i] = [0]*(n_tra-1)
        #temp = range(n_tra)
        #temp.remove(i)
        #for j in xrange(n_tra-1):
                #phi[i][j] = f(D[i][temp[j]])*M[j]
                #print f(D[i][temp[j]])
    #选路
    def FindSequence(i,k):
        phi[i] = [0]*(n_tra-1)
        temp = range(n_tra)
        temp.remove(i)
        for j in xrange(n_tra-1):
                phi[i][j] = f(D[i][temp[j]])*M[j]
        #前一个只留第k列
        if i > 0:
            for s in xrange(num_C[i]):
                if s != k:
                    for t in xrange(num_C[i-1]):
                        phi[i][i-1][t][s] = float('-inf')
        #后一个只留第k行
        if i < n_tra-1:
            for t in xrange(num_C[i]):
                if t != k:
                    for s in xrange(num_C[i+1]):
                        phi[i][i][t][s] = float('-inf')  
        #print phi[6]
        #动态规划
        fV = np.zeros((n_tra,max(num_C)))
        pre = np.zeros((n_tra,max(num_C),2))
        for t in xrange(num_C[0]):
            fV[0][t] = f(D[i][0])*N(C[i]['CPS'][t][1])
        for j in xrange(1,n_tra):
            for s in xrange(num_C[j]):
                for t in xrange(num_C[j-1]):
                    if fV[j-1][t]+phi[i][j-1][t][s] > fV[j][s] and w[j-1][t][s] != float('inf'): 
                        try:
                            src = C[j-1]['CPS'][t][0]
                            tgt = C[j]['CPS'][s][0]
                            #path = nx.shortest_path(C_nx,source = zg_mmap['s.id'][src] ,target = zg_mmap['s.id'][tgt])
                            path = allpath[zg_mmap['s.id'][src]][zg_mmap['s.id'][tgt]]
                            fV[j][s] = fV[j-1][t]+phi[i][j-1][t][s]
                            pre[j][s] = [j-1,t]
                        except:
                            continue
            #print fV
        fV_ik = max(fV[n_tra-1])
        c = list(fV[n_tra-1]).index(fV_ik)
        Sequence = [0]*n_tra
        Sequence[n_tra-1] = np.array([n_tra-1,c])
        #Sequence[n_tra-1] = [n_tra-1,c]
        for t in xrange(1,n_tra):
            Sequence[n_tra-1-t] = pre[Sequence[n_tra-t][0]][Sequence[n_tra-t][1]]
        #print fV
        #print pre
        return [fV_ik,Sequence]
       
    #投票(暂未考虑nv相同用fV解决冲突)
    votes = {'fV':[],'nv':[]}
    for i in xrange(len(num_C)):
        votes['fV'].append([])
        votes['nv'].append([])
        for j in xrange(num_C[i]):
            votes['fV'][i].append(0) 
            votes['nv'][i].append(0)
    count = 0
    for i in xrange(n_tra):
        for k in xrange(num_C[i]):
            [fV_ik,Sequence] = FindSequence(i, k)
            path=[]
            for cp in xrange(n_tra-1):
                try:
                    s = C[int(Sequence[cp][0])]['CPS'][int(Sequence[cp][1])][0]
                    e = C[int(Sequence[cp+1][0])]['CPS'][int(Sequence[cp+1][1])][0]
                    src = zg_mmap['s.id'][s]
                    tgt = zg_mmap['e.id'][e]
                    #path += nx.shortest_path(C_nx,source = src ,target = tgt)
                    path += allpath[src][tgt]
                    #if i==0 and k == 0:
                        ##print nx.shortest_path(C_nx,source = src ,target = tgt),src,tgt
                        #print allpath[src][tgt],src,tgt
                except:
                    print 'i=',i,'k=',k
                    count+=1
                    break
            path = list(set(path))
            #print path
            flag = 0
            for j in xrange(n_tra):
                if Sequence[j][0] != j:
                    flag += 1
            if votes['fV'][i][k] < fV_ik:
                votes['fV'][i][k] = fV_ik
            if flag == 0:
                for [p,q] in Sequence:
                    votes['nv'][int(p)][int(q)] += 1
    #绘制最终路径图
    Final_nx = nx.Graph()
    e = []
    for i in xrange(n_tra):
        m_votes = max(votes['nv'][i])
        #从重复最大投票中选取fV最大的
        a = [0]*len(votes['nv'][i])
        for v in xrange(len(votes['nv'][i])):
            if votes['nv'][i][v] ==  m_votes:
                a[v] = votes['fV'][i][v]
        k = a.index(max(a))
        index = C[i]['CPS'][k][0]
        Final_nx.add_weighted_edges_from([(zg_mmap['s.id'][index],zg_mmap['e.id'][index],zg_mmap['distance'][index])])
        #print index
        e.append(zg_mmap['e.id'][index])
    #for i in xrange(len(e)-1):
        #try:
            #path = nx.shortest_path(C_nx,source = e[i] ,target = e[i+1])
            #if len(path) >= 2:
                #for j in xrange(1,len(path)-1):
                    #Final_nx.add_weighted_edges_from([(path[j],path[j+1],1)])
        #except:
            #continue
    #Final_nx = max(nx.connected_component_subgraphs(Final_nx), key=len)
    nx.draw(Final_nx,position,with_labels=True,node_size = 10,width = 1)                   
    plt.show() 


#测试代码
test_track = {'lon':[104.764204,104.764513,104.764398,104.764694,104.765473,104.765923,104.766667,104.766805],
              'lat':[ 29.350574, 29.350602, 29.350958, 29.351147, 29.351463, 29.351486, 29.351478, 29.350898]}
IVMM(test_track,100)
