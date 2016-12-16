#-*- coding: UTF-8 -*- 
import pymssql
import CEasyMatching_sp as CEM
import time
#查询操作
gps_slct = pymssql.connect(host='.',user='sa',password='123456',database='GpsData',as_dict=True)
gps_updt = pymssql.connect(host='.',user='sa',password='123456',database='GpsData',as_dict=True)
st = time.time()
cur1 = gps_slct.cursor()
#SELECT 长连接查询操作（逐条方式获取数据）
sql1 = "select * from gps1 where gpsid between 8059999 and 8070001 order by gpsid"
cur1.execute(sql1)
print 'ok'
r_slct = cur1.fetchone()

cur2 = gps_updt.cursor()
#SELECT 长连接查询操作（逐条方式获取数据）
sql2 = "update gps1 set WayId=%d,SegId=%d,ID=%d,DeltaDis=%s,DeltaAng=%s  where gpsid=%d"

while r_slct:
    if r_slct['Longitude']!=0 and r_slct['Latitude']!=0:
        if r_slct['GpsSpeed']!= 0:
            r_EM = CEM.EasyMatching(float(r_slct['Longitude']), float(r_slct['Latitude']), r_slct['Angle'], 100, 5)
        else:
            r_EM = CEM.EasyMatching(float(r_slct['Longitude']), float(r_slct['Latitude']), 1000, 100, 5)
    else:
        r_EM = [0,0,0,100,181]    
    cur2.execute(sql2,(r_EM[0],r_EM[1],r_EM[2],r_EM[3],r_EM[4],r_slct['GpsId'])) 
    if r_slct['GpsId']%10000==0:
        gps_updt.commit()
        et = time.time()
        print r_slct['GpsId'],et-st
        st = time.time()
    r_slct = cur1.fetchone()
gps_slct.close()
gps_updt.close()

