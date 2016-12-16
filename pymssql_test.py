import pymssql
#查询操作
gps = pymssql.connect(host='192.168.1.106',user='sa',password='123456',database='GpsData')
cur = gps.cursor()
#SELECT 长连接查询操作（逐条方式获取数据）
sql = "select carid,unitid from carinfo where carid = '1'"
cur.execute(sql)
print cur.fetchall()

#使用的MSSQL2005,通过pymssql来连接的。把可能用到的数据库操作方式都总结如下，如果要用的时候就备查啦。网址：http://www.jb51.net/article/66686.htm
##!/usr/bin/env python
##coding=utf-8
#from __future__ import with_statement
#from contextlib import closing
#import inspect
#import pymssql
#import uuid
#import datetime
##查询操作
#with closing(pymssql.connect(host='localhost',user='sa',password='pppp',database='blogs')) as conn :
  #cur = conn.cursor()
  ##SELECT 长连接查询操作（逐条方式获取数据）
  #sql = "select * from pcontent"
  #cur.execute(sql)
  #for i in range(cur.rowcount):
    #print cur.fetchone()
  ##SELECT 短链接查询操作（一次查询将所有数据取出）
  #sql = "select * from pcontent"
  #cur.execute(sql)
  #print cur.fetchall()
  ##INSERT 
  #sql = "INSERT INTO pcontent(title)VAlUES(%s)"
  #uuidstr = str(uuid.uuid1())
  #cur.execute(sql,(uuidstr,))
  #conn.commit()
  #print cur._result
  ##INSERT 获取IDENTITY（在插入一个值，希望获得主键的时候经常用到，很不优雅的方式）
  #sql = "INSERT INTO pcontent(title)VAlUES(%s);SELECT @@IDENTITY"
  #uuidstr = str(uuid.uuid1())
  #cur.execute(sql,(uuidstr,))
  #print "arraysite:",cur.arraysize
  #print cur._result[1][2][0][0]#不知道具体的做法，目前暂时这样使用
  #conn.commit()
  ##Update
  #vl = '中国'
  #sql = 'update pcontent set title = %s where id=1'
  #cur.execute(sql,(vl,))
  #conn.commit()
  ##参数化查询这个是为了避免SQL攻击的
  #sql = "select * from pcontent where id=%d"
  #cur.execute(sql,(1,))
  #print cur.fetchall()
  ## 调用存储过程SP_GetALLContent 无参数
  #sql = "Exec SP_GetALLContent"
  #cur.execute(sql)
  #print cur.fetchall()
  ## 调用存储过程SP_GetContentByID 有参数的
  #sql = "Exec SP_GetContentByID %d"
  #cur.execute(sql,(3,))
  #print cur.fetchall()
  ##调用存储过程SP_AddContent 有output参数的(很不优雅的方式)
  #sql = "DECLARE @ID INT;EXEC SP_AddContent 'ddddd',@ID OUTPUT;SELECT @ID"
  #cur.execute(sql)
  #print cur._result
  
  