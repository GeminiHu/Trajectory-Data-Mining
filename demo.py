#本程序用10号出租车8月1日的数据实现了整个算法的简化框架。
#计算出的节点保存在demo_nodes
#因为只是demo，所以整个算法做出一些简化：
#1.只要计算出是拐点就认为是拐点，忽略投票机制；
#2.认为所有路都是直线，忽略立交桥，弧形路的影响；
#3.不考虑经纬度是球面坐标系，认为经纬度就是横纵坐标；
#4.考虑边权重（通过时间）时，因为记录数比较少所以求该路段全天的平均速度（不合理，仅为样例展示）。

import xlrd
import xlwt
from xlutils.copy import copy
import networkx as nx
import matplotlib.pyplot as plt
import math as m
import time
TIME_FORM = '%Y-%m-%d %X'
print 'This demo begans at '+time.strftime(TIME_FORM,time.localtime(time.time()))

node_radius = 500 #当两个点的距离小于该距离时，认为两个点在同一个拐点
#打开demo的数据表格
sta = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_data.xlsx')
table = sta.sheets()[0]
#创建demo_nodes表
demo_nodes = xlwt.Workbook()
dnd  = demo_nodes.add_sheet('01')
dnd.write(0,0,'NO.')
dnd.write(0,1,'Longitude')
dnd.write(0,2,'Latitude')
#创建demo_network表
demo_network = xlwt.Workbook()
dnx  = demo_network.add_sheet('01')
dnx.write(0,0,'Start')
dnx.write(0,1,'End')
dnx.write(0,2,'N')
dnx.write(0,3,'Sum_Velocity')
dnx.write(0,4,'Average_V')
dnx.write(0,5,'Distance')
dnx.write(0,6,'Average_T')

#开始处理数据以得到城市的数字地图
trajectory = [0]*1608 #记录该车8月1日当天的轨迹

#得到该城市所有的节点
#初始点作为一号节点
trajectory[0] = 1 
dnd.write(1,0,1)
dnd.write(1,1,table.cell(1,5).value)
dnd.write(1,2,table.cell(1,6).value)
#保存节点数据
demo_nodes.save('E://WSC225//GPS//GpsData//demo_nodes.xls')
No = 1 #初始化节点号
for i in xrange(2,1608):#demo一共有1608条记录
    delta = abs(table.cell(i,9).value-table.cell(i-1,9).value) #记录相邻两条数据的角度差
    if ((delta > 60 and delta < 120) or (delta > 240 and delta < 300)):
        #符合判定条件，则i条记录与i-1条记录中存在拐点
        k1 = m.tan(table.cell(i-1,9).value/180*m.pi) #i-1条记录的斜率
        k2 = m.tan(table.cell(i,9).value/180*m.pi)   #i条记录的斜率
        x1 = table.cell(i-1,5).value*10**5 #i-1条记录的经度
        x2 = table.cell(i,5).value*10**5   #i条记录的经度
        y1 = table.cell(i-1,6).value*10**5 #i-1条记录的维度
        y2 = table.cell(i,6).value*10**5   #i条记录的维度
        node_x = (y2-y1+k1*x1-k2*x2)/(k1-k2) #交点的经度
        node_y = (k1*y2-k2*y1+k1*k2*x1-k1*k2*x2)/(k1-k2) #交点的维度
        #获取可操作的节点数据
        demo_nodes = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_nodes.xls')
        copy_demo_nodes = copy(demo_nodes)
        dnd_w = copy_demo_nodes.get_sheet(0)  #获取可以写的excel副本
        dnd_r = demo_nodes.sheet_by_index(0)  #获取可以读的excel副本        
        #计算交点与各个已知节点的距离
        d_list = [0]*No
        for j in xrange(No):
            tx = dnd_r.cell(j+1,1).value*10**5  #j+1号节点的经度
            ty = dnd_r.cell(j+1,2).value*10**5  #j+1号节点的维度
            d_list[j] = m.sqrt((tx-node_x)**2+(ty-node_y)**2)
            #判断该节点是否与demo_nodes中已知节点距离大于node_radius
            #小于，则记录该节点的编号，修改trajectory[i]为该节点的编号
            if (d_list[j] < node_radius):
                trajectory[i] = j+1
                break
        #到每一个已知节点的距离都大于node_radius,即大于最小的
        #则计算节点的编号，添加节点的编号、经纬度到dnd，并修改trajectory[i]为新节点的编号
        if (min(d_list) > node_radius):
            No += 1
            dnd_w.write(No,0,No)
            dnd_w.write(No,1,node_x/(10**5))
            dnd_w.write(No,2,node_y/(10**5))
            trajectory[i] = No  
        copy_demo_nodes.save('E://WSC225//GPS//GpsData//demo_nodes.xls')

print 'Demo_nodes is built at '+time.strftime(TIME_FORM,time.localtime(time.time()))
            


#打开demo_nodes表供以后查询使用
demo_nodes = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_nodes.xls')
dnd = demo_nodes.sheets()[0]


#得到该城市的无权无向网络图 
G = [] #存储边
D = [] #存储边长度
sp = 1 #起点
ep = 0 #终点
for i in xrange(1,1608):
    if (trajectory[i] != 0 ):
        ep = trajectory[i] #终点则为这条边
        if ([sp,ep] not in G or [ep,sp] not in G): #如果这条边不在当前网络
            G.append([sp,ep]) #将该边加入网络
            #计算该边的长度，经纬度扩大十万倍使整数部分精度为米
            x1 = dnd.cell(sp,1).value*10**5 #起点的经度
            x2 = dnd.cell(ep,1).value*10**5 #终点的经度
            y1 = dnd.cell(sp,2).value*10**5 #起点的维度
            y2 = dnd.cell(ep,2).value*10**5 #终点的维度
            D.append(m.sqrt((x1-x2)**2+(y1-y2)**2))
            sp = ep #然后让终点变为起点，继续循环
            
#得到该城市的有权无向网络图
#网络初始化
for i in xrange(len(G)):
    dnx.write(i+1,0,G[i][0]) #起点
    dnx.write(i+1,1,G[i][1]) #终点
    dnx.write(i+1,2,0)    #该边记录个数
    dnx.write(i+1,3,0)    #总速度
    dnx.write(i+1,4,0)    #平均速度
    dnx.write(i+1,5,D[i]) #距离
    dnx.write(i+1,6,float('inf'))#平均时间
#保存网络数据 
demo_network.save('E://WSC225//GPS//GpsData//demo_network.xls')
#计算权重
temp_n = 1 #将轨迹用节点分成多段，记录一段的记录数，初始化从第一个节点开始，循环则从第二个节点开始
temp_sv = table.cell(1,8).value #初始化：第一个节点的速度
sp = 1 #起点
ep = 0 #终点
for i in xrange(1,1608):
    #获取可操作的网络数据
    demo_network = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_network.xls')
    copy_demo_network = copy(demo_network)
    dnx_w = copy_demo_network.get_sheet(0)  #获取可以写的excel副本
    dnx_r = demo_network.sheet_by_index(0)  #获取可以读的excel副本
    if (trajectory[i] != 0 ):
        ep = trajectory[i] #终点则为这条边
        #确定[sp,ep]在dnx_r中的行数
        if ([sp,ep] in G):
            m = G.index([sp,ep])+1
        if ([ep,sp] in G):
            m = G.index([ep,sp])+1            
        dnx_w.write(m,2,dnx_r.cell(m,2).value+temp_n)#修改该边记录个数
        if (dnx_r.cell(m,2).value+temp_n == 0):
            print sp,ep,dnx_r.cell(m,2).value, temp_n#--------------------------------------------
        dnx_w.write(m,3,dnx_r.cell(m,3).value+temp_sv)#修改总速度
        temp_n = 1 
        temp_sv = 0
        sp = ep
    else:#该点不是节点
        if (table.cell(i,8).value != 0):#速度不为零
            temp_n += 1           #有效车辆数加一
            temp_sv += table.cell(i,8).value#总速度加上该车速度
    copy_demo_network.save('E://WSC225//GPS//GpsData//demo_network.xls')

print 'Demo_network without weight  is built at '+time.strftime(TIME_FORM,time.localtime(time.time()))

####################################################################################################################
########以上代码生成的网络中会有一些问题：1.节点莫名其妙的N=0，2.边的起点与终点一样。但为了demo的快速完成，这些内容便被手动删除
######################################################################################################################
    
#计算平均速度与平均时间
G = [0]*201
for i in xrange(len(G)): #len(G) = 边的个数
    demo_network = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_network.xls')
    copy_demo_network = copy(demo_network)
    dnx_w = copy_demo_network.get_sheet(0)  #获取可以写的excel副本
    dnx_r = demo_network.sheet_by_index(0)  #获取可以读的excel副本
    average_v = dnx_r.cell(i+1,3).value/dnx_r.cell(i+1,2).value
    if (average_v != 0):
        average_t = dnx_r.cell(i+1,5).value/average_v
    else:
        average_t = 999999
    dnx_w.write(i+1,4,average_v)    #平均速度
    dnx_w.write(i+1,6,average_t)#平均时间
    copy_demo_network.save('E://WSC225//GPS//GpsData//demo_network.xls')

print 'Demo_network is built at '+time.strftime(TIME_FORM,time.localtime(time.time()))


#网络的可视化
#打开demo的数据表格
demo_network = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_network.xls')
dnx = demo_network.sheets()[0]
demo_nodes = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_nodes.xls')
dnd = demo_nodes.sheets()[0]
#建立网络
G_T = nx.Graph()   #建立以时间为权重的空无向图
G_T.position = {}  #G_T的节点定位
G_D = nx.Graph()   #建立以距离为权重的空无向图
G_D.position = {}  #G_D的节点定位
G = [0]*201
for i in xrange(len(G)):
    sp = int(dnx.cell(i+1,0).value)
    ep = int(dnx.cell(i+1,1).value)
    at = dnx.cell(i+1,6).value
    ad = dnx.cell(i+1,5).value
    G_T.add_weighted_edges_from([(sp,ep,at)])
    G_T.position[sp] = (dnd.cell(sp,1).value*10**6-104000000,dnd.cell(sp,2).value*10**6-104000000)
    G_T.position[ep] = (dnd.cell(ep,1).value*10**6-104000000,dnd.cell(ep,2).value*10**6-104000000)
    G_D.add_weighted_edges_from([(sp,ep,ad)])
    G_D.position[sp] = (dnd.cell(sp,1).value*10**6-104000000,dnd.cell(sp,2).value*10**6-104000000)
    G_D.position[ep] = (dnd.cell(ep,1).value*10**6-104000000,dnd.cell(ep,2).value*10**6-104000000)  

path_G_T=nx.all_pairs_shortest_path(G_T)
path_G_D=nx.all_pairs_shortest_path(G_D)
nx.draw(G_D,G_D.position,with_labels=False,node_size = 30)                   #绘制网络G_T
plt.show()
    
    
    

    
    
    

