#��������Ԥ�������������������Ľڵ㣬����test_nodes�ļ�
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

#���봦������ļ�
with open('E://WSC225//GPS//GpsData//processed_test_data.pickle', 'rb') as f_pickle:
   pd = pickle.load(f_pickle)
f_pickle.close()

#����test_nodes��
test_nodes = xlwt.Workbook()
tnd  = test_nodes.add_sheet('01')
tnd.write(0,0,'NO.')
tnd.write(0,1,'Longitude')
tnd.write(0,2,'Latitude')

#��Ԥ�������ݼ���ڵ�
for i in xrange(len(pd)):
   if len(pd[i]) > 3 :
      print pd[i]
      
   