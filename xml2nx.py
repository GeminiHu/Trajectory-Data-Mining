#�������ܣ�
#��1��	��xml��ͼ�����ֵ�zg_map����ʽΪs.id, s.lat, s.lon, e.id, e.lat, e.lon, way.id, segment.id,distance,angle,IDʮһ��
#��2��	��xml��ͼ����networkx�����浽���أ�ÿ���ڵ���Ϊid�������澭γ����Ϣ

import networkx as nx
import matplotlib.pyplot as plt
import pickle
import xml.dom.minidom
from math import radians, cos, sin, asin, sqrt 
import math as m
import time

# ʹ��minidom�������� XML ��ͼ
zigong = xml.dom.minidom.parse("I://zigong.xml")
zg = zigong.documentElement
nodes = zg.getElementsByTagName('node') #�ڵ�
ways = zg.getElementsByTagName('way')   #��·

nd = {} #ÿ������´��ž�γ��
w  = {} #ÿ������´��Ųο���
for i in xrange(len(nodes)):
    nd[int(nodes[i].getAttribute('id'))] = {'lat':float(nodes[i].getAttribute('lat')),'lon':float(nodes[i].getAttribute('lon'))}
for i in xrange(len(ways)):
    tgs = ways[i].getElementsByTagName('tag')
    temp = [] #��¼��ǰ��·tag��ʲôkֵ
    for j in xrange(len(tgs)):
        temp.append(tgs[j].getAttribute('k'))
    if not 'highway' in temp and len(tgs) != 0:
        continue   
    wayid = int(ways[i].getAttribute('id'))
    nds = ways[i].getElementsByTagName('nd')#way[i]�µĽڵ�
    w[wayid] = []
    for j in xrange(len(nds)):
        w[wayid].append(int(nds[j].getAttribute('ref')))

#�õ�����way��tag
tag = {}
notag = [] #û��tag��ǵ�wayid
nohighway = []#tag��û��highway�ĵ�·
for i in xrange(len(ways)):
    tgs = ways[i].getElementsByTagName('tag')
    temp = [] #��¼��ǰ��·tag��ʲôkֵ
    if len(tgs)==0:
        notag.append(int(ways[i].getAttribute('id')))
    for j in xrange(len(tgs)):
        if not tgs[j].getAttribute('k') in tag.keys():
            tag[tgs[j].getAttribute('k')] = []
            tag[tgs[j].getAttribute('k')].append(tgs[j].getAttribute('v'))
        else:
            if not tgs[j].getAttribute('v') in tag[tgs[j].getAttribute('k')]:
                tag[tgs[j].getAttribute('k')].append(tgs[j].getAttribute('v'))
        temp.append(tgs[j].getAttribute('k'))
    if not 'highway' in temp:
        nohighway.append(temp)

#�����������
def haversine(lon1, lat1, lon2, lat2): # ����1��γ��1������2��γ��2 ��ʮ���ƶ�����  
    """ 
    Calculate the great circle distance between two points  
    on the earth (specified in decimal degrees) 
    """  
    # ��ʮ���ƶ���ת��Ϊ����  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
  
    # haversine��ʽ  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # ����ƽ���뾶����λΪ����  
    return c * r * 1000 #�����λΪ��

#·�εĽǶ�0~360
def SegmentAngle (lon1, lat1, lon2, lat2):
    # ��ʮ���ƶ���ת��Ϊ����,����Ϊ0��  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])    
    cosc = sin(lat1)*sin(lat2)+cos(lat1)*cos(lat2)*cos(lon2-lon1)
    sinc = sqrt(1-cosc**2)
    sina = cos(lat2)*sin(lon2-lon1)/sinc
    if abs(sina)>1:
        sina = sina/abs(sina)
    angle = asin(sina)*180/m.pi
    a = lat2-lat1
    b = lon2-lon1 
    if a>0 and b>0:
        return angle
    if a<0:
        return -angle+180
    if a>0 and b<0:
        return angle+360
    if a==0 and b>0:
        return 90
    if a==0 and b<0:
        return 270  
    if b==0 and a>0:
        return 0
    if b==0 and a<0:
        return 180    


#������������ѡ�ߣ����ؾ������ѡ��
def Candinate(t_lon,t_lat,s_lon,s_lat,e_lon,e_lat,se):
    st = haversine(t_lon,t_lat,s_lon,s_lat)
    te = haversine(t_lon,t_lat,e_lon,e_lat)
    flag = (st**2+se**2-te**2)/(2*se**2)
    if flag <= 0:
        return {'dis':st,'lon':s_lon,'lat':s_lat}
    elif flag >= 1:
        return {'dis':te,'lon':e_lon,'lat':e_lat}
    else:
        return {'dis':m.sqrt(st**2-(flag*se)**2),
                'lon':flag*(e_lon-s_lon)+s_lon,
                'lat':flag*(e_lat-s_lat)+s_lat}    

    

zg_map = {} #�Թ��ĵ�ͼ����������0�����ͼ���ݵĵ�һ��Ϊ��Ϊ���õı����쳣����
zg_map['s.id'] = [0]
zg_map['s.lat'] = [0]
zg_map['s.lon'] = [0]
zg_map['e.id'] = [0]
zg_map['e.lat'] = [0]
zg_map['e.lon'] = [0]
zg_map['way.id'] = [0]
zg_map['segment.id'] = [0]
zg_map['distance'] = [0]
zg_map['angle'] = [0]
for wayid in w.keys():
    for segid in xrange(1,len(w[wayid])):
        dis = haversine(nd[w[wayid][segid-1]]['lon'], nd[w[wayid][segid-1]]['lat'], nd[w[wayid][segid]]['lon'], nd[w[wayid][segid]]['lat'])
        if dis > 0:
            zg_map['s.id'].append(w[wayid][segid-1])
            zg_map['s.lat'].append(nd[w[wayid][segid-1]]['lat'])
            zg_map['s.lon'].append(nd[w[wayid][segid-1]]['lon'])
            zg_map['e.id'].append(w[wayid][segid])
            zg_map['e.lat'].append(nd[w[wayid][segid]]['lat'])
            zg_map['e.lon'].append(nd[w[wayid][segid]]['lon'])
            zg_map['way.id'].append(wayid)
            zg_map['segment.id'].append(segid)  
            zg_map['distance'].append(dis)
            zg_map['angle'].append(SegmentAngle(nd[w[wayid][segid-1]]['lon'], nd[w[wayid][segid-1]]['lat'], nd[w[wayid][segid]]['lon'], nd[w[wayid][segid]]['lat']))        
zg_map['ID'] = range(len(zg_map['s.id'])) #ÿһ��·�ε�Ψһ��ʾ
        
zg_nx = nx.Graph() #�Թ���networkx����
zg_nx.position = {}
for seg in xrange(1,len(zg_map['s.id'])):
    distance = zg_map['distance'][seg]
    zg_nx.add_weighted_edges_from([(zg_map['s.id'][seg],zg_map['e.id'][seg],distance)])
    zg_nx.position[zg_map['s.id'][seg]] = (zg_map['s.lon'][seg],zg_map['s.lat'][seg])
    zg_nx.position[zg_map['e.id'][seg]] = (zg_map['e.lon'][seg],zg_map['e.lat'][seg])    
    

zg_mnx = max(nx.connected_component_subgraphs(zg_nx), key=len)#ȡ��ͼ�е������ͨͼ
zg_mmap = {}
zg_mnx_nd = zg_mnx.nodes()
zg_mmap['s.id'] = []
zg_mmap['s.lat'] = []
zg_mmap['s.lon'] = []
zg_mmap['e.id'] = []
zg_mmap['e.lat'] = []
zg_mmap['e.lon'] = []
zg_mmap['way.id'] = []
zg_mmap['segment.id'] = []
zg_mmap['distance'] = []
zg_mmap['angle'] = []
zg_mmap['ID'] = []
for i in xrange(len(zg_map['s.id'])):
    if (zg_map['s.id'][i] in zg_mnx_nd) and (zg_map['e.id'][i] in zg_mnx_nd):
        zg_mmap['s.id'].append(zg_map['s.id'][i])
        zg_mmap['s.lat'].append(zg_map['s.lat'][i])
        zg_mmap['s.lon'].append(zg_map['s.lon'][i])
        zg_mmap['e.id'].append(zg_map['e.id'][i])
        zg_mmap['e.lat'].append(zg_map['e.lat'][i])
        zg_mmap['e.lon'].append(zg_map['e.lon'][i])
        zg_mmap['way.id'].append(zg_map['way.id'][i])
        zg_mmap['segment.id'].append(zg_map['segment.id'][i])
        zg_mmap['distance'].append(zg_map['distance'][i])  
        zg_mmap['angle'].append(zg_map['angle'][i])
        zg_mmap['ID'].append(zg_map['ID'][i])


#����grid_map����ͼ�ֳ����������ڵ�ͼƥ���㷨��ʹ�ã����Ч��
zg_minlon = 104.036500
zg_maxlon = 105.429591
zg_minlat = 28.923760
zg_maxlat = 29.554397
dlon = (zg_maxlon-zg_minlon)/267.0 #���ȷֳ�267�ݺ�ÿ�ݵľ��ȱ仯
dlat = (zg_maxlat-zg_minlat)/138.0 #ά�ȷֳ�138�ݺ�ÿ�ݵ�ά�ȱ仯
grid_map = []
chosen_map = zg_map #ѡ����������grid_map�ĵ�ͼ
sta = []
for i in xrange(138):
    grid_map.append([])
    st = time.time()
    for j in xrange(267):
        grid_map[i].append({})
        grid_map[i][j]['s.id'] = [0]
        grid_map[i][j]['s.lat'] = [0]
        grid_map[i][j]['s.lon'] = [0]
        grid_map[i][j]['e.id'] = [0]
        grid_map[i][j]['e.lat'] = [0]
        grid_map[i][j]['e.lon'] = [0]
        grid_map[i][j]['way.id'] = [0]
        grid_map[i][j]['segment.id'] = [0]
        grid_map[i][j]['distance'] = [0]
        grid_map[i][j]['angle'] = [0]
        grid_map[i][j]['ID'] = [0]
        #���������ľ�γ��
        center_lon = zg_minlon + (j+0.5)*dlon
        center_lat = zg_minlat + (i+0.5)*dlat
        #��������r���ڵ�·��
        r = 255*sqrt(2) #����߳����509�ף���������������255*sqrt(2)�׷�Χ���ڵı߼���
        min_lon = center_lon-0.011
        max_lon = center_lon+0.011
        min_lat = center_lat-0.01
        max_lat = center_lat+0.01
        for index in xrange(1,len(chosen_map['s.id'])):
            dis_term = (chosen_map['distance'][index]>(1000-r))
            slon_term = (chosen_map['s.lon'][index]<max_lon and chosen_map['s.lon'][index]>min_lon)
            slat_term = (chosen_map['s.lat'][index]<max_lat and chosen_map['s.lat'][index]>min_lat)
            elon_term = (chosen_map['e.lon'][index]<max_lon and chosen_map['e.lon'][index]>min_lon)
            elat_term = (chosen_map['e.lat'][index]<max_lat and chosen_map['e.lat'][index]>min_lat)
            if dis_term or (slon_term and slat_term) or (elon_term and elat_term):    
                temp = Candinate(center_lon, center_lat, chosen_map['s.lon'][index], chosen_map['s.lat'][index], chosen_map['e.lon'][index],chosen_map['e.lat'][index],chosen_map['distance'][index])
                if temp['dis'] < r:
                    #print i,j,'ok'
                    grid_map[i][j]['s.id'].append(chosen_map['s.id'][index])
                    grid_map[i][j]['s.lat'].append(chosen_map['s.lat'][index])
                    grid_map[i][j]['s.lon'].append(chosen_map['s.lon'][index])
                    grid_map[i][j]['e.id'].append(chosen_map['e.id'][index])
                    grid_map[i][j]['e.lat'].append(chosen_map['e.lat'][index])
                    grid_map[i][j]['e.lon'].append(chosen_map['e.lon'][index])
                    grid_map[i][j]['way.id'].append(chosen_map['way.id'][index])
                    grid_map[i][j]['segment.id'].append(chosen_map['segment.id'][index])
                    grid_map[i][j]['distance'].append(chosen_map['distance'][index])
                    grid_map[i][j]['angle'].append(chosen_map['angle'][index]) 
                    grid_map[i][j]['ID'].append(chosen_map['ID'][index]) 
                    sta.append((chosen_map['way.id'][index],chosen_map['segment.id'][index]))
    et = time.time()
    print 'Program  has finished the %dth loop, cost time = %.6f'%(i,et-st)                
#���Դ��룺���������way.id������segment.id��·��
#for i in xrange(len(zg_mmap['distance'])):
    #for j in xrange(len(zg_mmap['distance'])):
        #if (i != j) and (zg_mmap['distance'][i] == zg_mmap['distance'][j]):
            #print '***************************'
            #print (zg_mmap['s.id'][i],zg_mmap['s.lat'][i],zg_mmap['s.lon'][i],zg_mmap['e.id'][i],zg_mmap['e.lat'][i],zg_mmap['e.lon'][i],zg_mmap['way.id'][i],zg_mmap['segment.id'][i],zg_mmap['distance'][i])
            #print (zg_mmap['s.id'][j],zg_mmap['s.lat'][j],zg_mmap['s.lon'][j],zg_mmap['e.id'][j],zg_mmap['e.lat'][j],zg_mmap['e.lon'][j],zg_mmap['way.id'][j],zg_mmap['segment.id'][j],zg_mmap['distance'][j])
        

              
zigong = [nd,w,zg_map,zg_nx,zg_nx.position,zg_mnx,zg_mmap,grid_map] 
# 0 nd��ԭʼxml�ļ����нڵ���ɵ��ֵ䣬ÿ���ڵ��о��ȡ�γ������
# 1 w ��ԭʼxml�ļ����е�·��ɵ��ֵ䣬ÿ��������洢�Ÿõ�·�ϵĲο���
# 2 zg_map ����������ԭʼ���е�ͼ�ֵ䣬������s.id, s.lat, s.lon, e.id, e.lat, e.lon, way.id, segment.id,distance,angle,IDʮһ��
# 3 zg_nx  ��zg_map�Ľڵ�ͱ���networkx.Graph()�洢���ļ���
# 4 zg_nx.position ��zg_nx���нڵ�ľ�γ����Ϣ�����ֵ��ʽ�洢
# 5 zg_mnx ��ԭʼzg_nx��ͼ�е������ͨ��ͼnetworkx�ļ�
# 6 zg_mmap ��ԭʼzg_map�е������ͨ��ͼ�ֵ�
# 7 grid_map: �����������Ժ���Թ���ͼ
with open('E://WSC225//GPS//GpsData//zigong.pickle', 'wb') as f_pickle:
    pickle.dump(zigong, f_pickle)
f_pickle.close() 

nx.draw(zg_nx,zg_nx.position,with_labels=False,node_size = 10,width = 1)                   
plt.show()
#nx.draw(zg_mnx,zg_nx.position,with_labels=False,node_size = 10,width = 1)                   
#plt.show()

        
    
    
    
    
    





