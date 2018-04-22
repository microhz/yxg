# -*- coding:utf-8 -*-
import sys
sys.path.append("./yxg/model")
import Workers
import json
import pymysql

def getByCondition(** kargs) :
    sql = "SELECT * FROM workers"

    condition = ""
    isExsitCondition = False
    if kargs.get('id') is not None :
        isExsitCondition = True
        condition = " id = " + str(kargs.get('id'))
    if kargs.get('name') is not None :
        if isExsitCondition :
            condition = condition + " AND 姓名 LIKE '%" + kargs.get('name') + "%'"
        else :
            isExsitCondition = True
            condition = " 姓名 LIKE '%" + kargs.get('name') + "%'"
        
    if kargs.get('tel') is not None :
        if isExsitCondition :
            condition = condition + " AND 电话 = " + kargs.get('tel')
        else :
            isExsitCondition = True
            condition = " 电话 = " + kargs.get('tel')

    if isExsitCondition :
        sql = sql + " WHERE " + condition

    result = []
    try :
        result = execute_sql(sql)
    except Exception as e:
        print('db error : msg ' + str(e))

    workers_list = []
    for _worker in result :
        worker = Workers.Workers(id = _worker.get('id'), name = _worker.get('姓名'), tel = _worker.get('电话'), address = _worker.get('通讯地址'))
        workers_list.append(worker.__dict__)
    return workers_list


def insertWorkers(** args) :
    workers = Workers.Workers(name = args.get('name'), tel = args.get('tel'), address = args.get('address'))
    sql = "INSERT INTO workers (姓名,电话,通讯地址) VALUES ('%s','%s','%s')" % (workers.name, workers.tel, workers.address)
    execute_sql(sql)
    

def execute_sql(sql):
    conn = pymysql.connect(host="192.168.1.104",
                           user="root",
                           password="root",
                           database="premetheus",
                           port=3306,
                           charset='utf8')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    print('execute sql ' + sql)
    try :
        cur.execute(sql)
        conn.commit()
    except Exception as e :
        print('db error , msg = ' + str(e))
        raise e
    if cur.rowcount == 0:
        return []
    result = cur._rows
    print('execute result ' + str(result))
    cur.close()
    print('end')
    conn.close()
    return result

        

