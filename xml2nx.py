#本程序功能：
#（1）	将xml地图存入字典zg_map，格式为s.id, s.lat, s.lon, e.id, e.lat, e.lon, way.id, segment.id,distance,angle,ID十一项
#（2）	将xml地图存入networkx并保存到本地，每个节点名为id，并保存经纬度信息

import networkx as nx
import matplotlib.pyplot as plt
import pickle
import xml.dom.minidom
from math import radians, cos, sin, asin, sqrt 
import math as m
import time

# 使用minidom解析器打开 XML 地图
zigong = xml.dom.minidom.parse("I://zigong.xml")
zg = zigong.documentElement
nodes = zg.getElementsByTagName('node') #节点
ways = zg.getElementsByTagName('way')   #道路

nd = {} #每个编号下存着经纬度
w  = {} #每个编号下存着参考点
for i in xrange(len(nodes)):
    nd[int(nodes[i].getAttribute('id'))] = {'lat':float(nodes[i].getAttribute('lat')),'lon':float(nodes[i].getAttribute('lon'))}
for i in xrange(len(ways)):
    tgs = ways[i].getElementsByTagName('tag')
    temp = [] #记录当前道路tag有什么k值
    for j in xrange(len(tgs)):
        temp.append(tgs[j].getAttribute('k'))
    if not 'highway' in temp and len(tgs) != 0:
        continue   
    wayid = int(ways[i].getAttribute('id'))
    nds = ways[i].getElementsByTagName('nd')#way[i]下的节点
    w[wayid] = []
    for j in xrange(len(nds)):
        w[wayid].append(int(nds[j].getAttribute('ref')))

#得到所有way的tag
tag = {}
notag = [] #没有tag标记的wayid
nohighway = []#tag中没有highway的道路
for i in xrange(len(ways)):
    tgs = ways[i].getElementsByTagName('tag')
    temp = [] #记录当前道路tag有什么k值
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

#路段的角度0~360
def SegmentAngle (lon1, lat1, lon2, lat2):
    # 将十进制度数转化为弧度,正北为0度  
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
        return {'dis':m.sqrt(st**2-(flag*se)**2),
                'lon':flag*(e_lon-s_lon)+s_lon,
                'lat':flag*(e_lat-s_lat)+s_lat}    

    

zg_map = {} #自贡的地图，以下所有0代表地图数据的第一条为人为设置的备用异常数据
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
zg_map['ID'] = range(len(zg_map['s.id'])) #每一个路段的唯一标示
        
zg_nx = nx.Graph() #自贡的networkx数据
zg_nx.position = {}
for seg in xrange(1,len(zg_map['s.id'])):
    distance = zg_map['distance'][seg]
    zg_nx.add_weighted_edges_from([(zg_map['s.id'][seg],zg_map['e.id'][seg],distance)])
    zg_nx.position[zg_map['s.id'][seg]] = (zg_map['s.lon'][seg],zg_map['s.lat'][seg])
    zg_nx.position[zg_map['e.id'][seg]] = (zg_map['e.lon'][seg],zg_map['e.lat'][seg])    
    

zg_mnx = max(nx.connected_component_subgraphs(zg_nx), key=len)#取地图中的最大连通图
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


#生成grid_map将地图分成若干网格，在地图匹配算法中使用，提高效率
zg_minlon = 104.036500
zg_maxlon = 105.429591
zg_minlat = 28.923760
zg_maxlat = 29.554397
dlon = (zg_maxlon-zg_minlon)/267.0 #经度分成267份后，每份的经度变化
dlat = (zg_maxlat-zg_minlat)/138.0 #维度分成138份后，每份的维度变化
grid_map = []
chosen_map = zg_map #选择用来生成grid_map的地图
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
        #该网格中心经纬度
        center_lon = zg_minlon + (j+0.5)*dlon
        center_lat = zg_minlat + (i+0.5)*dlat
        #距离中心r米内的路段
        r = 255*sqrt(2) #网格边长最大509米，所以搜索距中心255*sqrt(2)米范围以内的边即可
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
#测试代码：输出有两个way.id或两个segment.id的路段
#for i in xrange(len(zg_mmap['distance'])):
    #for j in xrange(len(zg_mmap['distance'])):
        #if (i != j) and (zg_mmap['distance'][i] == zg_mmap['distance'][j]):
            #print '***************************'
            #print (zg_mmap['s.id'][i],zg_mmap['s.lat'][i],zg_mmap['s.lon'][i],zg_mmap['e.id'][i],zg_mmap['e.lat'][i],zg_mmap['e.lon'][i],zg_mmap['way.id'][i],zg_mmap['segment.id'][i],zg_mmap['distance'][i])
            #print (zg_mmap['s.id'][j],zg_mmap['s.lat'][j],zg_mmap['s.lon'][j],zg_mmap['e.id'][j],zg_mmap['e.lat'][j],zg_mmap['e.lon'][j],zg_mmap['way.id'][j],zg_mmap['segment.id'][j],zg_mmap['distance'][j])
        

              
zigong = [nd,w,zg_map,zg_nx,zg_nx.position,zg_mnx,zg_mmap,grid_map] 
# 0 nd：原始xml文件所有节点组成的字典，每个节点有经度、纬度数据
# 1 w ：原始xml文件所有道路组成的字典，每条边下面存储着该道路上的参考点
# 2 zg_map ：处理过后的原始城市地图字典，其中有s.id, s.lat, s.lon, e.id, e.lat, e.lon, way.id, segment.id,distance,angle,ID十一项
# 3 zg_nx  ：zg_map的节点和边以networkx.Graph()存储的文件，
# 4 zg_nx.position ：zg_nx所有节点的经纬度信息，以字典格式存储
# 5 zg_mnx ：原始zg_nx地图中的最大连通子图networkx文件
# 6 zg_mmap ：原始zg_map中的最大连通子图字典
# 7 grid_map: 将网络网格化以后的自贡地图
with open('E://WSC225//GPS//GpsData//zigong.pickle', 'wb') as f_pickle:
    pickle.dump(zigong, f_pickle)
f_pickle.close() 

nx.draw(zg_nx,zg_nx.position,with_labels=False,node_size = 10,width = 1)                   
plt.show()
#nx.draw(zg_mnx,zg_nx.position,with_labels=False,node_size = 10,width = 1)                   
#plt.show()

        
    
    
    
    
    





