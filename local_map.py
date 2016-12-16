#将grid_map中的数据，每九个格子合并在一起，得到local_map
import pickle
import time
import numpy as np
import copy
#读grid_map
with open('E://WSC225//GPS//GpsData//zigong.pickle', 'rb') as f_pickle:
    zigong = pickle.load(f_pickle)
f_pickle.close() 
grid_map = zigong[7]
local_map = []
local_map = copy.deepcopy(grid_map)
for i in xrange(138):
    st = time.time()
    segtime=[0,0,0,0]
    num_local = []
    for j in xrange(267):
        flag1 = time.time()
        #将除自身以外的八个相邻网格的信息加入字典
        #wayrecord = [] #记录不重复的way.id和segment.id
        if (i in range(1,137)) and (j in range(1,266)):
            loop = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
        elif i==0 and j==0:
            loop = [(i,j+1),(i+1,j),(i+1,j+1)]
        elif i==0 and j==266:
            loop = [(i,j-1),(i+1,j-1),(i+1,j)]
        elif i==137 and j==0:
            loop = [(i-1,j),(i-1,j+1),(i,j+1)]
        elif i==137 and j==266:
            loop = [(i-1,j-1),(i-1,j),(i,j-1)] 
        elif i==0 and j in range(1,267):
            loop = [(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
        elif i==137 and j in range(1,267):
            loop = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1)]  
        elif i in range(1,137) and j==0:
            loop = [(i-1,j),(i-1,j+1),(i,j+1),(i+1,j),(i+1,j+1)] 
        elif i in range(1,137) and j==266:
            loop = [(i-1,j-1),(i-1,j),(i,j-1),(i+1,j-1),(i+1,j)]   
        else:
            try:
                raise MyError #自己抛出一个异常
            except MyError:
                print 'a error' 
        flag2 = time.time()
        for (m,n) in loop:
            nn = len(grid_map[m][n]['s.id'])
            for k in xrange(nn):
                if grid_map[m][n]['ID'][k] not in local_map[i][j]['ID']:
                    local_map[i][j]['s.id'].append(grid_map[m][n]['s.id'][k])
                    local_map[i][j]['s.lat'].append(grid_map[m][n]['s.lat'][k])
                    local_map[i][j]['s.lon'].append(grid_map[m][n]['s.lon'][k])
                    local_map[i][j]['e.id'].append(grid_map[m][n]['e.id'][k])
                    local_map[i][j]['e.lat'].append(grid_map[m][n]['e.lat'][k])
                    local_map[i][j]['e.lon'].append(grid_map[m][n]['e.lon'][k])
                    local_map[i][j]['way.id'].append(grid_map[m][n]['way.id'][k])
                    local_map[i][j]['segment.id'].append(grid_map[m][n]['segment.id'][k])
                    local_map[i][j]['distance'].append(grid_map[m][n]['distance'][k])
                    local_map[i][j]['angle'].append(grid_map[m][n]['angle'][k])
                    local_map[i][j]['ID'].append(grid_map[m][n]['ID'][k])
                    #for index in xrange(len(grid_map[m][n]['way.id'])):
                        #wayrecord.append((grid_map[m][n]['way.id'][index],grid_map[m][n]['segment.id'][index]))
        flag3 = time.time()
        #wayrecord = list(set(wayrecord))
        #num = len(local_map[i][j]['s.id'])
        #remove = []#记录需要移除记录的标号
        #for index in xrange(num):
            #if (local_map[i][j]['way.id'][index],local_map[i][j]['segment.id'][index]) in wayrecord:
                #wayrecord.remove((local_map[i][j]['way.id'][index],local_map[i][j]['segment.id'][index]))
            #else:
                #remove.append(index)
        #remove.sort(reverse=True)
        flag4 = time.time()
        #for rmv in remove:
            #local_map[i][j]['s.id'].remove(local_map[i][j]['s.id'][rmv])
            #local_map[i][j]['s.lat'].remove(local_map[i][j]['s.lat'][rmv])
            #local_map[i][j]['s.lon'].remove(local_map[i][j]['s.lon'][rmv])
            #local_map[i][j]['e.id'].remove(local_map[i][j]['e.id'][rmv])
            #local_map[i][j]['e.lat'].remove(local_map[i][j]['e.lat'][rmv])
            #local_map[i][j]['e.lon'].remove(local_map[i][j]['e.lon'][rmv])
            #local_map[i][j]['way.id'].remove(local_map[i][j]['way.id'][rmv])
            #local_map[i][j]['segment.id'].remove(local_map[i][j]['segment.id'][rmv])
            #local_map[i][j]['distance'].remove(local_map[i][j]['distance'][rmv])
            #local_map[i][j]['angle'].remove(local_map[i][j]['angle'][rmv]) 
        flag5 = time.time()
        segtime[0]+=flag2-flag1
        segtime[1]+=flag3-flag2
        segtime[2]+=flag4-flag3
        segtime[3]+=flag5-flag4
        num_local.append(len(local_map[i][j]['ID']))
    et = time.time()
    print 'Program  has finished the %dth loop, cost time = %.6f'%(i,et-st)
    print 'Fourfold cost %.3f,%.3f,%.3f,%.3f respectively'%(segtime[0],segtime[1],segtime[2],segtime[3])
    print 'Mean of the number of segments in grid of %dth row is %.2f '%(i,np.mean(num_local))
    print ''

with open('E://WSC225//GPS//GpsData//local_map.pickle', 'wb') as f_pickle:
    pickle.dump(local_map, f_pickle)
f_pickle.close() 

        
        
                