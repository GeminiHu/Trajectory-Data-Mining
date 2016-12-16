#本程序实现对test_data文件的预处理
#提取出来的数据以分组形势存储，每一组都是一组时间连续的数据
#注意事项：test_data文件在被处理之前需要把GPS坐标，车速，方向角完全重合的记录删去重复项

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

#打开test_data的数据表格
test_data = xlrd.open_workbook('E://WSC225//GPS//GpsData//test_data.xlsx')
td = test_data.sheets()[0]
td_nr = td.nrows #获取td表的行数

pd = [] #processed_data存储处理过的数据
dt = 0.001 #判断两条记录是否相邻的时间差阀值

#初始化
temp = [] #存储当前分组的数据
temp.append((td.cell(1,6).value,td.cell(1,7).value,td.cell(1,10).value,td.cell(1,11).value)) #添加第一条记录的GPS坐标，车速，方向角
pre_carid = td.cell(1,1).value #记录前一条记录的carid
pre_time = td.cell(1,2).value #记录前一条记录的GPS时间

print 'The loop began at '+time.strftime(TIME_FORM,time.localtime(time.time()))

#遍历表格处理数据
for i in xrange(2,td_nr):
#for i in xrange(2,1000): #测试代码
    carid = td.cell(i,1).value #记录当前记录的carid
    time = td.cell(i,2).value #记录当前记录的GPS时间
    if carid > pre_carid: #carid发生变化，进行初始化
        if len(temp) > 1:
            pd.append(temp) #当前组记录数大于1，则存储改组记录
        temp = [] #重置当前分组
        temp.append((td.cell(i,6).value,td.cell(i,7).value,td.cell(i,10).value,td.cell(i,11).value)) #添加当前记录的GPS坐标，车速，方向角到新分组
    else: #carid不变
        if abs(time-pre_time) < dt: #如果时间差小于阀值，则没有记录缺失
            temp.append((td.cell(i,6).value,td.cell(i,7).value,td.cell(i,10).value,td.cell(i,11).value)) #添加当前记录的GPS坐标，车速，方向角到当前分组
        else:
            if len(temp) > 1:
                pd.append(temp) #当前组记录数大于1，则存储改组记录
            temp = [] #重置当前分组
            temp.append((td.cell(i,6).value,td.cell(i,7).value,td.cell(i,10).value,td.cell(i,11).value)) #添加当前记录的GPS坐标，车速，方向角到新分组
    pre_carid = carid #记录当前记录的carid
    pre_time = time #记录当前记录的GPS时间            

#存储处理后的数据到硬盘
with open('E://WSC225//GPS//GpsData//processed_test_data.pickle', 'wb') as f_pickle:
    pickle.dump(pd, f_pickle)
f_pickle.close() 



