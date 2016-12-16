#-*- coding: UTF-8 -*- 
#简单版的mapmatching

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle
import math as m
from math import radians, cos, sin, asin, sqrt 
import xlrd
import time
from haversine import haversine


#记录开始时间
TIME_FORM = '%Y-%m-%d %X'
print '*********************This program began at '+time.strftime(TIME_FORM,time.localtime(time.time())) +'*************************'
print ' '

#读取道路网络
with open('E://WSC225//GPS//GpsData//zigong.pickle', 'rb') as f_pickle:
    zigong = pickle.load(f_pickle)
f_pickle.close() 
#Candidates Preparation
zg_mmap = zigong[6]
zg_mnx = zigong[5]
zg_nx = zigong[3]
zg_map = zigong[2]
position = zigong[4]
with open('E://WSC225//GPS//GpsData//local_map.pickle', 'rb') as f_pickle:
    local_map = pickle.load(f_pickle)
f_pickle.close() 

zg_minlon = 104.036500
zg_maxlon = 105.429591
zg_minlat = 28.923760
zg_maxlat = 29.554397
dlon = (zg_maxlon-zg_minlon)/267.0 #经度分成267份后，每份的经度变化
dlat = (zg_maxlat-zg_minlat)/138.0 #维度分成138份后，每份的维度变化

with open('E://WSC225//GPS//GpsData//results_excel2.pickle', 'rb') as f_pickle:
    std = pickle.load(f_pickle)
f_pickle.close()


#输入采样点与候选边，返回距离与候选点
def Candinate(t_lon,t_lat,s_lon,s_lat,e_lon,e_lat,se):
    st = haversine(t_lon,t_lat,s_lon,s_lat)
    te = haversine(t_lon,t_lat,e_lon,e_lat)
    flag = (st**2+se**2-te**2)/(2*se**2)
    if flag <= 0:
        return {'dis':st,'lon':s_lon,'lat':s_lat}
    elif flag >= 1:
        return {'dis':te,'lon':e_lon,'lat':e_lat}
    else:
        return {'dis':m.sqrt(abs(st**2-(flag*se)**2)),
                'lon':flag*(e_lon-s_lon)+s_lon,
                'lat':flag*(e_lat-s_lat)+s_lat}

def EasyMatching (trajectory,r,max_Candinate):
    """ 
    trajectory存储路径的字典，r候选路径的选择范围（单位米）
    """  
    #print '*********************EasyMatching began at '+time.strftime(TIME_FORM,time.localtime(time.time())) +'*************************'
    #print ' '    
    n_tra = len(trajectory['lon']) #采样点个数
    #确定CPS、CP
    C = []
    for i in xrange(n_tra):
        map_i = int((trajectory['lat'][i]-zg_minlat)/dlat)
        map_j = int((trajectory['lon'][i]-zg_minlon)/dlon)
        test_localmaps.append((map_i,map_j))
        chosen_map = local_map[map_i][map_j]
        C.append({'CPS':[],'CP':[]})
        rank = [] #记录第i个采样点前五个最近候选点的距离
        min_lon = trajectory['lon'][i]-0.011
        max_lon = trajectory['lon'][i]+0.011
        min_lat = trajectory['lat'][i]-0.01
        max_lat = trajectory['lat'][i]+0.01
        for j in xrange(len(chosen_map['s.id'])):
            dis_term = (chosen_map['distance'][j]>(1000-r))
            slon_term = (chosen_map['s.lon'][j]<max_lon and chosen_map['s.lon'][j]>min_lon)
            slat_term = (chosen_map['s.lat'][j]<max_lat and chosen_map['s.lat'][j]>min_lat)
            elon_term = (chosen_map['e.lon'][j]<max_lon and chosen_map['e.lon'][j]>min_lon)
            elat_term = (chosen_map['e.lat'][j]<max_lat and chosen_map['e.lat'][j]>min_lat)
            cdtn = dis_term or (slon_term and slat_term and elon_term and elat_term)
            if cdtn:
                temp = Candinate(trajectory['lon'][i], trajectory['lat'][i], chosen_map['s.lon'][j], chosen_map['s.lat'][j], chosen_map['e.lon'][j],chosen_map['e.lat'][j],chosen_map['distance'][j])
                if temp['dis'] < r:
                    if len(C[i]['CPS']) < max_Candinate:#限制候选路段数量
                        C[i]['CPS'].append((chosen_map['ID'][j],temp['dis'],chosen_map['angle'][j]))
                        C[i]['CP'].append((temp['lon'],temp['lat']))
                        rank.append(temp['dis'])
                    else:
                        if temp['dis'] < max(rank):
                            for n in xrange(max_Candinate):
                                if C[i]['CPS'][n][1] == max(rank):
                                    C[i]['CPS'].remove(C[i]['CPS'][n])
                                    C[i]['CP'].remove(C[i]['CP'][n])
                                    rank.remove(max(rank))
                                    C[i]['CPS'].append((chosen_map['ID'][j],temp['dis'],chosen_map['angle'][j])) 
                                    C[i]['CP'].append((temp['lon'],temp['lat']))
                                    rank.append(temp['dis'])
                                    break   
        #没有候选边就人为填充数据                        
        if len(C[i]['CPS'])==0:
            C[i]['CPS'].append((0,0,trajectory['angle'][i])) #j是候选边在zg_map中的index
            C[i]['CP'].append((trajectory['lon'][i],trajectory['lat'][i]))
    #每个采样点的候选点个数
    num_C = [0]*n_tra
    for i in xrange(n_tra):
        num_C[i] = len(C[i]['CP'])  
    #选择候选边
    d = [0]*n_tra
    a = [0]*n_tra
    for i in xrange(n_tra):
        d[i] = []
        a[i] = []
        for k in xrange(num_C[i]):
            d[i].append(round(C[i]['CPS'][k][1],2))
            t = abs(trajectory['angle'][i]-C[i]['CPS'][k][2])
            a[i].append(round(min([t,360-t]),1))
    p = [0]*n_tra
    for i in xrange(n_tra):
        p[i] = []
        if num_C[i]==1:
            p[i].append(1) #如果只有一个候选点，被选中的概率为1
            continue
        for k in xrange(num_C[i]):
            if a[i][k] > 90:
                p[i].append(0)
                continue
            try:
                r1 = (max(d[i])-d[i][k])/(max(d[i])-min(d[i]))
            except ZeroDivisionError:
                r1 = 1
            try:
                r2 = (max(a[i])-a[i][k])/(max(a[i])-min(a[i]))
            except ZeroDivisionError:
                r2 = 1
            p[i].append(0.5*r1+0.5*r2)
    result = []
    for i in xrange(n_tra):
        if max(p[i]) > 0.8:
            k = p[i].index(max(p[i]))
        else:
            k = d[i].index(min(d[i]))
        result.append(C[i]['CPS'][k][0]) 
    #绘制最终路径图
    Final_nx = nx.DiGraph() #可视化后加粗端为终点 
    Final_edges = []
    Normal_edges = []
    nodelist = []
    node_labels = {}
    edge_labels = {}
    for i in xrange(n_tra):
        Final_nx.add_node('%s'%i)
        nodelist.append('%s'%i)
        node_labels['%s'%i] = (i,int(trajectory['angle'][i]),result[i])
        position['%s'%i] = (trajectory['lon'][i],trajectory['lat'][i])
        map_i = test_localmaps[i][0]
        map_j = test_localmaps[i][1]
        for index in xrange(len(local_map[map_i][map_j]['s.id'])):
            Final_nx.add_weighted_edges_from([(local_map[map_i][map_j]['s.id'][index],local_map[map_i][map_j]['e.id'][index],local_map[map_i][map_j]['distance'][index])]) 
            edge_labels[(local_map[map_i][map_j]['s.id'][index],local_map[map_i][map_j]['e.id'][index])] = local_map[map_i][map_j]['ID'][index]
            if local_map[map_i][map_j]['s.id'][index]!= 0 and local_map[map_i][map_j]['e.id'][index] !=0:
                Normal_edges.append((local_map[map_i][map_j]['s.id'][index],local_map[map_i][map_j]['e.id'][index]))
    for i in xrange(step):
        index = result[i]
        if index != 0:
            Final_edges.append((zg_map['s.id'][index],zg_map['e.id'][index]))
    Final_nx.remove_node(0)
    #输出debug用的信息
    for i in xrange(n_tra):
        print 
        print 'i=',i, 'angle=',trajectory['angle'][i]
        for k in xrange(num_C[i]):
            index = C[i]['CPS'][k][0]
            print 'k=',k,'ID:',zg_map['ID'][index],'angle:',("%6.1f"%C[i]['CPS'][k][2]), 'a:',("%6.2f"%a[i][k]),'d:',("%6.3f"%d[i][k]),'p:',("%3.5f"%p[i][k]),'road:',zg_map['way.id'][index],zg_map['segment.id'][index]    
    if monitor != result:
        print '**************************************************************************************************************************'
        print "******************************************************ERROR***************************************************************"
        print '**************************************************************************************************************************' 
        for i in xrange(step):
            if monitor[i] != result:
                print 'monitor[%d] = %d, result[%d] = %d'%(i,monitor[i],i,result[i])
    nx.draw_networkx_edges(Final_nx,position,edgelist=Normal_edges,width=1,edge_color='k')
    nx.draw_networkx_edges(Final_nx,position,edgelist=Final_edges,width=3,alpha=0.5,edge_color='r') 
    nx.draw_networkx_nodes(Final_nx,position,nodelist=Final_nx.nodes(),node_size=20)
    nx.draw_networkx_labels(Final_nx,position,labels=node_labels,font_size=15,font_family='sans-serif')
    edge_labels.pop((0,0))
    nx.draw_networkx_edge_labels(Final_nx,position,edge_labels=edge_labels)
    plt.title('Sample Points From %d To %d'%(z*step,z*step+step-1),fontsize = '30')
    plt.show() 

print '*********************Main function began at '+time.strftime(TIME_FORM,time.localtime(time.time())) +'*************************'
print ' '

sta = xlrd.open_workbook('E://2.xls')
table = sta.sheets()[0]

step = 5
for z in xrange(215,1130/step):
    test = {'lon':[],'lat':[],'angle':[]}
    test_localmaps = []
    monitor = std[z*step:(z+1)*step]
    for i in xrange(z*step+1,(z+1)*step+1):
        test['lon'].append(table.cell(i,5).value)
        test['lat'].append(table.cell(i,6).value)
        test['angle'].append(table.cell(i,9).value)
    EasyMatching(test,100,5) 
