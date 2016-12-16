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

#选择要使用的地图与网络
#chosen_map = zg_map
#chosen_nx = zg_nx


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
    #sta_time = [0]*5
    for i in xrange(n_tra):
        #global flag
        #flag+=1
        map_i = int((trajectory['lat'][i]-zg_minlat)/dlat)
        map_j = int((trajectory['lon'][i]-zg_minlon)/dlon)
        chosen_map = local_map[map_i][map_j]
        C.append({'CPS':[],'CP':[]})
        rank = [] #记录第i个采样点前五个最近候选点的距离
        min_lon = trajectory['lon'][i]-0.011
        max_lon = trajectory['lon'][i]+0.011
        min_lat = trajectory['lat'][i]-0.01
        max_lat = trajectory['lat'][i]+0.01
        for j in xrange(len(chosen_map['s.id'])):
            #sta_time[0] = time.time()
            dis_term = (chosen_map['distance'][j]>(1000-r))
            slon_term = (chosen_map['s.lon'][j]<max_lon and chosen_map['s.lon'][j]>min_lon)
            slat_term = (chosen_map['s.lat'][j]<max_lat and chosen_map['s.lat'][j]>min_lat)
            elon_term = (chosen_map['e.lon'][j]<max_lon and chosen_map['e.lon'][j]>min_lon)
            elat_term = (chosen_map['e.lat'][j]<max_lat and chosen_map['e.lat'][j]>min_lat)
            cdtn = dis_term or (slon_term and slat_term and elon_term and elat_term)
            #sta_time[1] = time.time()
            if cdtn:
                #sta_time[3] = time.time()
                temp = Candinate(trajectory['lon'][i], trajectory['lat'][i], chosen_map['s.lon'][j], chosen_map['s.lat'][j], chosen_map['e.lon'][j],chosen_map['e.lat'][j],chosen_map['distance'][j])
                #sta_time[4] = time.time()
                #count[flag]+=1
                if temp['dis'] < r:
                    if len(C[i]['CPS']) < max_Candinate:#限制候选路段数量
                        C[i]['CPS'].append((j,temp['dis'],chosen_map['angle'][j]))
                        C[i]['CP'].append((temp['lon'],temp['lat']))
                        rank.append(temp['dis'])
                    else:
                        if temp['dis'] < max(rank):
                            for n in xrange(max_Candinate):
                                if C[i]['CPS'][n][1] == max(rank):
                                    C[i]['CPS'].remove(C[i]['CPS'][n])
                                    C[i]['CP'].remove(C[i]['CP'][n])
                                    rank.remove(max(rank))
                                    C[i]['CPS'].append((j,temp['dis'],chosen_map['angle'][j])) #j是候选边在zg_map中的index
                                    C[i]['CP'].append((temp['lon'],temp['lat']))
                                    rank.append(temp['dis'])
                                    break
            #sta_time[2] = time.time()
            #for zz in xrange(4):
                #tt[zz] += (sta_time[zz+1]-sta_time[zz])         
        #没有候选边就人为填充数据                        
        if len(C[i]['CPS'])==0:
            C[i]['CPS'].append((0,0,trajectory['angle'][i])) #j是候选边在zg_map中的index
            C[i]['CP'].append((trajectory['lon'][i],trajectory['lat'][i]))
    #每个采样点的候选点个数
    num_C = [0]*n_tra
    for i in xrange(n_tra):
        num_C[i] = len(C[i]['CP'])  
    #测试6选错边的原因
    #for k in xrange(num_C[6]):
        #j = C[6]['CPS'][k][0]
        #print chosen_map['s.id'][j],chosen_map['e.id'][j],chosen_map['angle'][j]    
    #建立候选图
    #C_nx = nx.Graph() 
    #for sample_index in xrange(n_tra):
        #for CPS_index in xrange(len(C[sample_index]['CPS'])):
            #index = C[sample_index]['CPS'][CPS_index][0]
            #C_nx.add_weighted_edges_from([(chosen_map['s.id'][index],chosen_map['e.id'][index],chosen_map['distance'][index])])
            ##print chosen_map['s.id'][index],chosen_map['e.id'][index]
    ##C_nx = max(nx.connected_component_subgraphs(C_nx), key=len)
    #for i in xrange(n_tra):
        #C_nx.add_node(i,color = 'g',size = 300)
        #position[i] = (trajectory['lon'][i],trajectory['lat'][i])
    #nx.draw(C_nx,position,with_labels = True,node_size = 10,width = 1)                   
    #plt.show()
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
    #绘制最终路径图
    Final_nx = nx.Graph()
    for i in xrange(n_tra):
        #allp.append(max(p[i]))
        if max(p[i]) > 0.8:
            k = p[i].index(max(p[i]))
        else:
            k = d[i].index(min(d[i]))
        index = C[i]['CPS'][k][0]
        #if index==0:
            #global num_0
            #num_0 += 1 
        if index != 0: #如果第i个采样点，没有候选路段
            Final_nx.add_weighted_edges_from([(chosen_map['s.id'][index],chosen_map['e.id'][index],chosen_map['distance'][index])])
            #print 'i=',i,'s-e:',chosen_map['s.id'][index],chosen_map['e.id'][index]
        #print i,chosen_map['s.id'][index],chosen_map['e.id'][index],trajectory['angle'][i]
        #print chosen_map['way.id'][index],chosen_map['segment.id'][index]
        #Final_nx.add_node(i,color = 'g',size = 300)
        #e.append(chosen_map['e.id'][index])    
    nx.draw(Final_nx,position,with_labels=False,node_size = 10,width = 1)
    plt.show() 
    #print '*********************This work finish at '+time.strftime(TIME_FORM,time.localtime(time.time())) +'*************************'
    #print ' '
    #输出debug用的信息
    #for i in xrange(n_tra):
        #print 
        #print 'i=',i, 'angle=',trajectory['angle'][i]
        #for k in xrange(num_C[i]):
            #index = C[i]['CPS'][k][0]
            #print 'k=',k,'s-e:',chosen_map['s.id'][index],chosen_map['e.id'][index],'angle:',("%6.1f"%C[i]['CPS'][k][2]), 'a:',("%6.2f"%a[i][k]),'d:',("%6.3f"%d[i][k]),'p:',("%3.5f"%p[i][k]),'road:',chosen_map['way.id'][index],chosen_map['segment.id'][index]
            
    #nx.draw(C_nx,position,with_labels = True,node_size = 10,width = 1)                   
    #plt.show()  
    return chosen_map['ID'][index]

print '*********************Main function began at '+time.strftime(TIME_FORM,time.localtime(time.time())) +'*************************'
print ' '
#sta = xlrd.open_workbook('E://2.xls')
#table = sta.sheets()[0]


#global num_0
##num_0 = 0
##for i in xrange(954,966):
##for i in xrange(666,677):
#for z in [68]:#[49,63,65,66,67,68,76]:
##for z in xrange(24,37):
    #test = {'lon':[],'lat':[],'angle':[]}
    ##print 'z=',z*10
    #for i in xrange(z*10+1,z*10+11):
        #test['lon'].append(table.cell(i,5).value)
        #test['lat'].append(table.cell(i,6).value)
        #test['angle'].append(table.cell(i,9).value)
    #EasyMatching(test,900,5000)

#print num_0
    


sta = xlrd.open_workbook('E://2.xls')
table = sta.sheets()[0]
#allp = []
#count = [0]*1130
#global falg
#flag = -1
results = []
#tt = np.zeros(4)
for z in xrange(56):
    test = {'lon':[],'lat':[],'angle':[]}
    for i in xrange(z*20+1,z*20+21):
        test['lon'].append(table.cell(i,5).value)
        test['lat'].append(table.cell(i,6).value)
        test['angle'].append(table.cell(i,9).value)
        EasyMatching(test,100,5) 
st = time.time()    
#for i in xrange(1,1131):
    #test = {'lon':[],'lat':[],'angle':[]}
    #test['lon'].append(table.cell(i,5).value)
    #test['lat'].append(table.cell(i,6).value)
    #test['angle'].append(table.cell(i,9).value)
    #results.append( EasyMatching(test,100,5))
et = time.time()    
print '*********************This work finish at '+time.strftime(TIME_FORM,time.localtime(time.time())) +',cost = %.3fs*************************'%(et-st)
#print tt
print ' '

with open('E://WSC225//GPS//GpsData//results_excel2.pickle', 'rb') as f_pickle:
    std = pickle.load(f_pickle)
f_pickle.close() 

d = np.array(results)- np.array(std)
print 'The difference between std and results is %.2f'%np.min(d)

#with open('E://WSC225//GPS//GpsData//results_excel2.pickle', 'wb') as f_pickle:
    #pickle.dump(results, f_pickle)
#f_pickle.close() 
