#������ʵ�ֶ�test_data�ļ���Ԥ����
#��ȡ�����������Է������ƴ洢��ÿһ�鶼��һ��ʱ������������
#ע�����test_data�ļ��ڱ�����֮ǰ��Ҫ��GPS���꣬���٣��������ȫ�غϵļ�¼ɾȥ�ظ���

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

#��test_data�����ݱ��
test_data = xlrd.open_workbook('E://WSC225//GPS//GpsData//test_data.xlsx')
td = test_data.sheets()[0]
td_nr = td.nrows #��ȡtd�������

pd = [] #processed_data�洢�����������
dt = 0.001 #�ж�������¼�Ƿ����ڵ�ʱ��ֵ

#��ʼ��
temp = [] #�洢��ǰ���������
temp.append((td.cell(1,6).value,td.cell(1,7).value,td.cell(1,10).value,td.cell(1,11).value)) #��ӵ�һ����¼��GPS���꣬���٣������
pre_carid = td.cell(1,1).value #��¼ǰһ����¼��carid
pre_time = td.cell(1,2).value #��¼ǰһ����¼��GPSʱ��

print 'The loop began at '+time.strftime(TIME_FORM,time.localtime(time.time()))

#�������������
for i in xrange(2,td_nr):
#for i in xrange(2,1000): #���Դ���
    carid = td.cell(i,1).value #��¼��ǰ��¼��carid
    time = td.cell(i,2).value #��¼��ǰ��¼��GPSʱ��
    if carid > pre_carid: #carid�����仯�����г�ʼ��
        if len(temp) > 1:
            pd.append(temp) #��ǰ���¼������1����洢�����¼
        temp = [] #���õ�ǰ����
        temp.append((td.cell(i,6).value,td.cell(i,7).value,td.cell(i,10).value,td.cell(i,11).value)) #��ӵ�ǰ��¼��GPS���꣬���٣�����ǵ��·���
    else: #carid����
        if abs(time-pre_time) < dt: #���ʱ���С�ڷ�ֵ����û�м�¼ȱʧ
            temp.append((td.cell(i,6).value,td.cell(i,7).value,td.cell(i,10).value,td.cell(i,11).value)) #��ӵ�ǰ��¼��GPS���꣬���٣�����ǵ���ǰ����
        else:
            if len(temp) > 1:
                pd.append(temp) #��ǰ���¼������1����洢�����¼
            temp = [] #���õ�ǰ����
            temp.append((td.cell(i,6).value,td.cell(i,7).value,td.cell(i,10).value,td.cell(i,11).value)) #��ӵ�ǰ��¼��GPS���꣬���٣�����ǵ��·���
    pre_carid = carid #��¼��ǰ��¼��carid
    pre_time = time #��¼��ǰ��¼��GPSʱ��            

#�洢���������ݵ�Ӳ��
with open('E://WSC225//GPS//GpsData//processed_test_data.pickle', 'wb') as f_pickle:
    pickle.dump(pd, f_pickle)
f_pickle.close() 



