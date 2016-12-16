#-*- coding: UTF-8 -*- 
#使用C与python混合编程的EasyMatching


import numpy as np
import pickle
import xlrd
import time
import math as m
from haversine import haversine,condition,Candinate


#记录开始时间
TIME_FORM = '%Y-%m-%d %X'
print '*********************This program began at '+time.strftime(TIME_FORM,time.localtime(time.time())) +'*************************'
print ' '

with open('E://WSC225//GPS//GpsData//local_map.pickle', 'rb') as f_pickle:
    local_map = pickle.load(f_pickle)
f_pickle.close() 

zg_minlon = 104.036500
zg_maxlon = 105.429591
zg_minlat = 28.923760
zg_maxlat = 29.554397
dlon = (zg_maxlon-zg_minlon)/267.0 #经度分成267份后，每份的经度变化
dlat = (zg_maxlat-zg_minlat)/138.0 #维度分成138份后，每份的维度变化

def EasyMatching (trajectory,r,max_Candinate):
    """ 
    trajectory存储路径的字典，r候选路径的选择范围（单位米）
    """  
    n_tra = len(trajectory['lon']) #采样点个数
    #确定CPS、CP
    C = []
    for i in xrange(n_tra):
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
            cdtn = condition(chosen_map['distance'][j],r,\
                             chosen_map['s.lon'][j],max_lon,chosen_map['s.lon'][j],min_lon,\
                             chosen_map['s.lat'][j],max_lat,chosen_map['s.lat'][j],min_lat,\
                             chosen_map['e.lon'][j],max_lon,chosen_map['e.lon'][j],min_lon,\
                             chosen_map['e.lat'][j],max_lat,chosen_map['e.lat'][j],min_lat)
            if cdtn:
                temp_dis,temp_lon,temp_lat = Candinate(trajectory['lon'][i], trajectory['lat'][i], chosen_map['s.lon'][j], chosen_map['s.lat'][j], chosen_map['e.lon'][j],chosen_map['e.lat'][j],chosen_map['distance'][j])              
                if temp_dis < r:
                    if len(C[i]['CPS']) < max_Candinate:#限制候选路段数量
                        C[i]['CPS'].append((j,temp_dis,chosen_map['angle'][j]))
                        C[i]['CP'].append((temp_lon,temp_lat))
                        rank.append(temp_dis)
                    else:
                        if temp_dis < max(rank):
                            for n in xrange(max_Candinate):
                                if C[i]['CPS'][n][1] == max(rank):
                                    C[i]['CPS'].remove(C[i]['CPS'][n])
                                    C[i]['CP'].remove(C[i]['CP'][n])
                                    rank.remove(max(rank))
                                    C[i]['CPS'].append((j,temp_dis,chosen_map['angle'][j])) #j是候选边在chosen_map中的index
                                    C[i]['CP'].append((temp_lon,temp_lat))
                                    rank.append(temp_dis)
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
    #绘制最终路径图
    for i in xrange(n_tra):
        if max(p[i]) > 0.8:
            k = p[i].index(max(p[i]))
        else:
            k = d[i].index(min(d[i]))
        index = C[i]['CPS'][k][0]
    return chosen_map['ID'][index]

print '*********************Main function began at '+time.strftime(TIME_FORM,time.localtime(time.time())) +'*************************'
print ' '
sta = xlrd.open_workbook('E://2.xls')
table = sta.sheets()[0]
#results = []
st = time.time()    
for i in xrange(1,1131):
    test = {'lon':[],'lat':[],'angle':[]}
    test['lon'].append(table.cell(i,5).value)
    test['lat'].append(table.cell(i,6).value)
    test['angle'].append(table.cell(i,9).value)
    EasyMatching(test,100.0,5)
    #results.append( EasyMatching(test,100.0,5)) #参数r必须是浮点型
et = time.time()    
print '*********************This work finish at '+time.strftime(TIME_FORM,time.localtime(time.time())) +',cost = %.3fs*************************'%(et-st)
print ' '

#with open('E://WSC225//GPS//GpsData//results_excel2.pickle', 'rb') as f_pickle:
    #std = pickle.load(f_pickle)
#f_pickle.close() 

#d = np.array(results)- np.array(std)
#print 'The difference between std and results is %.2f'%(np.max(d)-np.min(d)+np.mean(d))

