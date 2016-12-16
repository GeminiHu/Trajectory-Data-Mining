#��������10�ų��⳵8��1�յ�����ʵ���������㷨�ļ򻯿�ܡ�
#������Ľڵ㱣����demo_nodes
#��Ϊֻ��demo�����������㷨����һЩ�򻯣�
#1.ֻҪ������ǹյ����Ϊ�ǹյ㣬����ͶƱ���ƣ�
#2.��Ϊ����·����ֱ�ߣ����������ţ�����·��Ӱ�죻
#3.�����Ǿ�γ������������ϵ����Ϊ��γ�Ⱦ��Ǻ������ꣻ
#4.���Ǳ�Ȩ�أ�ͨ��ʱ�䣩ʱ����Ϊ��¼���Ƚ����������·��ȫ���ƽ���ٶȣ���������Ϊ����չʾ����

import xlrd
import xlwt
from xlutils.copy import copy
import networkx as nx
import matplotlib.pyplot as plt
import math as m
import time
TIME_FORM = '%Y-%m-%d %X'
print 'This demo begans at '+time.strftime(TIME_FORM,time.localtime(time.time()))

node_radius = 500 #��������ľ���С�ڸþ���ʱ����Ϊ��������ͬһ���յ�
#��demo�����ݱ��
sta = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_data.xlsx')
table = sta.sheets()[0]
#����demo_nodes��
demo_nodes = xlwt.Workbook()
dnd  = demo_nodes.add_sheet('01')
dnd.write(0,0,'NO.')
dnd.write(0,1,'Longitude')
dnd.write(0,2,'Latitude')
#����demo_network��
demo_network = xlwt.Workbook()
dnx  = demo_network.add_sheet('01')
dnx.write(0,0,'Start')
dnx.write(0,1,'End')
dnx.write(0,2,'N')
dnx.write(0,3,'Sum_Velocity')
dnx.write(0,4,'Average_V')
dnx.write(0,5,'Distance')
dnx.write(0,6,'Average_T')

#��ʼ���������Եõ����е����ֵ�ͼ
trajectory = [0]*1608 #��¼�ó�8��1�յ���Ĺ켣

#�õ��ó������еĽڵ�
#��ʼ����Ϊһ�Žڵ�
trajectory[0] = 1 
dnd.write(1,0,1)
dnd.write(1,1,table.cell(1,5).value)
dnd.write(1,2,table.cell(1,6).value)
#����ڵ�����
demo_nodes.save('E://WSC225//GPS//GpsData//demo_nodes.xls')
No = 1 #��ʼ���ڵ��
for i in xrange(2,1608):#demoһ����1608����¼
    delta = abs(table.cell(i,9).value-table.cell(i-1,9).value) #��¼�����������ݵĽǶȲ�
    if ((delta > 60 and delta < 120) or (delta > 240 and delta < 300)):
        #�����ж���������i����¼��i-1����¼�д��ڹյ�
        k1 = m.tan(table.cell(i-1,9).value/180*m.pi) #i-1����¼��б��
        k2 = m.tan(table.cell(i,9).value/180*m.pi)   #i����¼��б��
        x1 = table.cell(i-1,5).value*10**5 #i-1����¼�ľ���
        x2 = table.cell(i,5).value*10**5   #i����¼�ľ���
        y1 = table.cell(i-1,6).value*10**5 #i-1����¼��ά��
        y2 = table.cell(i,6).value*10**5   #i����¼��ά��
        node_x = (y2-y1+k1*x1-k2*x2)/(k1-k2) #����ľ���
        node_y = (k1*y2-k2*y1+k1*k2*x1-k1*k2*x2)/(k1-k2) #�����ά��
        #��ȡ�ɲ����Ľڵ�����
        demo_nodes = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_nodes.xls')
        copy_demo_nodes = copy(demo_nodes)
        dnd_w = copy_demo_nodes.get_sheet(0)  #��ȡ����д��excel����
        dnd_r = demo_nodes.sheet_by_index(0)  #��ȡ���Զ���excel����        
        #���㽻���������֪�ڵ�ľ���
        d_list = [0]*No
        for j in xrange(No):
            tx = dnd_r.cell(j+1,1).value*10**5  #j+1�Žڵ�ľ���
            ty = dnd_r.cell(j+1,2).value*10**5  #j+1�Žڵ��ά��
            d_list[j] = m.sqrt((tx-node_x)**2+(ty-node_y)**2)
            #�жϸýڵ��Ƿ���demo_nodes����֪�ڵ�������node_radius
            #С�ڣ����¼�ýڵ�ı�ţ��޸�trajectory[i]Ϊ�ýڵ�ı��
            if (d_list[j] < node_radius):
                trajectory[i] = j+1
                break
        #��ÿһ����֪�ڵ�ľ��붼����node_radius,��������С��
        #�����ڵ�ı�ţ���ӽڵ�ı�š���γ�ȵ�dnd�����޸�trajectory[i]Ϊ�½ڵ�ı��
        if (min(d_list) > node_radius):
            No += 1
            dnd_w.write(No,0,No)
            dnd_w.write(No,1,node_x/(10**5))
            dnd_w.write(No,2,node_y/(10**5))
            trajectory[i] = No  
        copy_demo_nodes.save('E://WSC225//GPS//GpsData//demo_nodes.xls')

print 'Demo_nodes is built at '+time.strftime(TIME_FORM,time.localtime(time.time()))
            


#��demo_nodes���Ժ��ѯʹ��
demo_nodes = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_nodes.xls')
dnd = demo_nodes.sheets()[0]


#�õ��ó��е���Ȩ��������ͼ 
G = [] #�洢��
D = [] #�洢�߳���
sp = 1 #���
ep = 0 #�յ�
for i in xrange(1,1608):
    if (trajectory[i] != 0 ):
        ep = trajectory[i] #�յ���Ϊ������
        if ([sp,ep] not in G or [ep,sp] not in G): #��������߲��ڵ�ǰ����
            G.append([sp,ep]) #���ñ߼�������
            #����ñߵĳ��ȣ���γ������ʮ��ʹ�������־���Ϊ��
            x1 = dnd.cell(sp,1).value*10**5 #���ľ���
            x2 = dnd.cell(ep,1).value*10**5 #�յ�ľ���
            y1 = dnd.cell(sp,2).value*10**5 #����ά��
            y2 = dnd.cell(ep,2).value*10**5 #�յ��ά��
            D.append(m.sqrt((x1-x2)**2+(y1-y2)**2))
            sp = ep #Ȼ�����յ��Ϊ��㣬����ѭ��
            
#�õ��ó��е���Ȩ��������ͼ
#�����ʼ��
for i in xrange(len(G)):
    dnx.write(i+1,0,G[i][0]) #���
    dnx.write(i+1,1,G[i][1]) #�յ�
    dnx.write(i+1,2,0)    #�ñ߼�¼����
    dnx.write(i+1,3,0)    #���ٶ�
    dnx.write(i+1,4,0)    #ƽ���ٶ�
    dnx.write(i+1,5,D[i]) #����
    dnx.write(i+1,6,float('inf'))#ƽ��ʱ��
#������������ 
demo_network.save('E://WSC225//GPS//GpsData//demo_network.xls')
#����Ȩ��
temp_n = 1 #���켣�ýڵ�ֳɶ�Σ���¼һ�εļ�¼������ʼ���ӵ�һ���ڵ㿪ʼ��ѭ����ӵڶ����ڵ㿪ʼ
temp_sv = table.cell(1,8).value #��ʼ������һ���ڵ���ٶ�
sp = 1 #���
ep = 0 #�յ�
for i in xrange(1,1608):
    #��ȡ�ɲ�������������
    demo_network = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_network.xls')
    copy_demo_network = copy(demo_network)
    dnx_w = copy_demo_network.get_sheet(0)  #��ȡ����д��excel����
    dnx_r = demo_network.sheet_by_index(0)  #��ȡ���Զ���excel����
    if (trajectory[i] != 0 ):
        ep = trajectory[i] #�յ���Ϊ������
        #ȷ��[sp,ep]��dnx_r�е�����
        if ([sp,ep] in G):
            m = G.index([sp,ep])+1
        if ([ep,sp] in G):
            m = G.index([ep,sp])+1            
        dnx_w.write(m,2,dnx_r.cell(m,2).value+temp_n)#�޸ĸñ߼�¼����
        if (dnx_r.cell(m,2).value+temp_n == 0):
            print sp,ep,dnx_r.cell(m,2).value, temp_n#--------------------------------------------
        dnx_w.write(m,3,dnx_r.cell(m,3).value+temp_sv)#�޸����ٶ�
        temp_n = 1 
        temp_sv = 0
        sp = ep
    else:#�õ㲻�ǽڵ�
        if (table.cell(i,8).value != 0):#�ٶȲ�Ϊ��
            temp_n += 1           #��Ч��������һ
            temp_sv += table.cell(i,8).value#���ٶȼ��ϸó��ٶ�
    copy_demo_network.save('E://WSC225//GPS//GpsData//demo_network.xls')

print 'Demo_network without weight  is built at '+time.strftime(TIME_FORM,time.localtime(time.time()))

####################################################################################################################
########���ϴ������ɵ������л���һЩ���⣺1.�ڵ�Ī�������N=0��2.�ߵ�������յ�һ������Ϊ��demo�Ŀ�����ɣ���Щ���ݱ㱻�ֶ�ɾ��
######################################################################################################################
    
#����ƽ���ٶ���ƽ��ʱ��
G = [0]*201
for i in xrange(len(G)): #len(G) = �ߵĸ���
    demo_network = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_network.xls')
    copy_demo_network = copy(demo_network)
    dnx_w = copy_demo_network.get_sheet(0)  #��ȡ����д��excel����
    dnx_r = demo_network.sheet_by_index(0)  #��ȡ���Զ���excel����
    average_v = dnx_r.cell(i+1,3).value/dnx_r.cell(i+1,2).value
    if (average_v != 0):
        average_t = dnx_r.cell(i+1,5).value/average_v
    else:
        average_t = 999999
    dnx_w.write(i+1,4,average_v)    #ƽ���ٶ�
    dnx_w.write(i+1,6,average_t)#ƽ��ʱ��
    copy_demo_network.save('E://WSC225//GPS//GpsData//demo_network.xls')

print 'Demo_network is built at '+time.strftime(TIME_FORM,time.localtime(time.time()))


#����Ŀ��ӻ�
#��demo�����ݱ��
demo_network = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_network.xls')
dnx = demo_network.sheets()[0]
demo_nodes = xlrd.open_workbook('E://WSC225//GPS//GpsData//demo_nodes.xls')
dnd = demo_nodes.sheets()[0]
#��������
G_T = nx.Graph()   #������ʱ��ΪȨ�صĿ�����ͼ
G_T.position = {}  #G_T�Ľڵ㶨λ
G_D = nx.Graph()   #�����Ծ���ΪȨ�صĿ�����ͼ
G_D.position = {}  #G_D�Ľڵ㶨λ
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
nx.draw(G_D,G_D.position,with_labels=False,node_size = 30)                   #��������G_T
plt.show()
    
    
    

    
    
    

