import pymssql
#��ѯ����
gps = pymssql.connect(host='192.168.1.106',user='sa',password='123456',database='GpsData')
cur = gps.cursor()
#SELECT �����Ӳ�ѯ������������ʽ��ȡ���ݣ�
sql = "select carid,unitid from carinfo where carid = '1'"
cur.execute(sql)
print cur.fetchall()

#ʹ�õ�MSSQL2005,ͨ��pymssql�����ӵġ��ѿ����õ������ݿ������ʽ���ܽ����£����Ҫ�õ�ʱ��ͱ���������ַ��http://www.jb51.net/article/66686.htm
##!/usr/bin/env python
##coding=utf-8
#from __future__ import with_statement
#from contextlib import closing
#import inspect
#import pymssql
#import uuid
#import datetime
##��ѯ����
#with closing(pymssql.connect(host='localhost',user='sa',password='pppp',database='blogs')) as conn :
  #cur = conn.cursor()
  ##SELECT �����Ӳ�ѯ������������ʽ��ȡ���ݣ�
  #sql = "select * from pcontent"
  #cur.execute(sql)
  #for i in range(cur.rowcount):
    #print cur.fetchone()
  ##SELECT �����Ӳ�ѯ������һ�β�ѯ����������ȡ����
  #sql = "select * from pcontent"
  #cur.execute(sql)
  #print cur.fetchall()
  ##INSERT 
  #sql = "INSERT INTO pcontent(title)VAlUES(%s)"
  #uuidstr = str(uuid.uuid1())
  #cur.execute(sql,(uuidstr,))
  #conn.commit()
  #print cur._result
  ##INSERT ��ȡIDENTITY���ڲ���һ��ֵ��ϣ�����������ʱ�򾭳��õ����ܲ����ŵķ�ʽ��
  #sql = "INSERT INTO pcontent(title)VAlUES(%s);SELECT @@IDENTITY"
  #uuidstr = str(uuid.uuid1())
  #cur.execute(sql,(uuidstr,))
  #print "arraysite:",cur.arraysize
  #print cur._result[1][2][0][0]#��֪�������������Ŀǰ��ʱ����ʹ��
  #conn.commit()
  ##Update
  #vl = '�й�'
  #sql = 'update pcontent set title = %s where id=1'
  #cur.execute(sql,(vl,))
  #conn.commit()
  ##��������ѯ�����Ϊ�˱���SQL������
  #sql = "select * from pcontent where id=%d"
  #cur.execute(sql,(1,))
  #print cur.fetchall()
  ## ���ô洢����SP_GetALLContent �޲���
  #sql = "Exec SP_GetALLContent"
  #cur.execute(sql)
  #print cur.fetchall()
  ## ���ô洢����SP_GetContentByID �в�����
  #sql = "Exec SP_GetContentByID %d"
  #cur.execute(sql,(3,))
  #print cur.fetchall()
  ##���ô洢����SP_AddContent ��output������(�ܲ����ŵķ�ʽ)
  #sql = "DECLARE @ID INT;EXEC SP_AddContent 'ddddd',@ID OUTPUT;SELECT @ID"
  #cur.execute(sql)
  #print cur._result
  
  