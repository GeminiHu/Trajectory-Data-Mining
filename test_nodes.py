#本代码用预处理过的数据生成网络的节点，存于test_nodes文件
import xlrd
import xlwt
from xlutils.copy import copy
import networkx as nx
import matplotlib.pyplot as plt
import math as m
import time
import pickle

TIME_FORM = '%Y-%m-%d %X'
print 'This program began at '+time.strftime(TIME_FORM,time.localtime(time.time()))

#载入处理过的文件
with open('E://WSC225//GPS//GpsData//processed_test_data.pickle', 'rb') as f_pickle:
   pd = pickle.load(f_pickle)
f_pickle.close()

#创建test_nodes表
test_nodes = xlwt.Workbook()
tnd  = test_nodes.add_sheet('01')
tnd.write(0,0,'NO.')
tnd.write(0,1,'Longitude')
tnd.write(0,2,'Latitude')

#用预处理数据计算节点
for i in xrange(len(pd)):
   if len(pd[i]) > 3 :
      print pd[i]
      
   