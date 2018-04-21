# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse

# 查询信息：
import pymysql
import pandas as pd


def convice_dic_sql(dictory, table_name):
    sql_con = []
    sql_val = []
    for key in dictory.keys():
        condition = table_name[0] + '.' + key + ' LIKE %s '
        value = '%' + dictory[key] + '%'
        sql_con.append(condition)
        sql_val.append(value)

    string = 'AND '.join(sql_con)

    return string, sql_val


def worker_from_area(string):
    # 查询（目标地区）---（师傅信息）
    """ string = "a.province like '%北京%'" """

    sql_select = "SELECT w.id, w.姓名, w.电话, a.province, a.city, a.county " \
                 "FROM workers AS w, area AS a, workers_area AS wa " \
                 "WHERE wa.area_id=a.id AND wa.workers_id=w.id AND %s GROUP BY w.id" % string

    return sql_select


def worker_from_service(string):
    # 查询（目标服务）---（师傅信息）
    """  string1 = 's.主类别 LIKE '%家庭维修%'' """
    sql_select = "SELECT w.id, w.姓名, w.电话, s.主类别, s.类目, s.详情 " \
                 "FROM workers AS w, service AS s, workers_service AS ws " \
                 "WHERE w.id=ws.workers_id AND s.id=ws.service_id AND %s GROUP BY w.id GROUP BY w.id" % string

    return sql_select


def area_from_workers_name(name):
    # 查询（目标师傅名字）--（基本信息--姓名/城市）
    """根据师傅名字查询   string = '陈海云'   """

    sql = "SELECT w.id, w.姓名, w.电话, a.province, a.city, a.county " \
          "FROM workers AS w, area AS a, workers_area AS wa " \
          "WHERE w.姓名='%s' AND a.id =wa.area_id AND w.id=wa.workers_id GROUP BY a.id" % name

    return sql


def service_from_workers_name(name):
    # 查询（目标师傅名字）--（基本服务）
    """根据师傅名字查询   string = '陈海云'   """

    sql = "SELECT w.id, w.姓名, w.电话, s.详情 " \
          "FROM workers AS w, service AS s, workers_service AS ws " \
          "WHERE w.姓名='%s' AND s.id=ws.service_id AND w.id=ws.workers_id GROUP BY s.id" % name

    return sql


def worker_all_message_from_name(name):
    # 根据名字  --查询师傅的所有信息

    sql_select = "SELECT wm.workers_id, wm.`姓名`, wm.`电话`, a.province, a.city, a.county, s.service_kind_id, s.`主类别`," \
                 "s.`类目`, s.`详情` FROM area AS a, workers_message AS wm, " \
                 "(SELECT wa.area_id, wa.workers_id FROM worker_and_area AS wa WHERE wa.workers_id IN " \
                 "(SELECT workers_message.workers_id FROM workers_message WHERE workers_message.`姓名`='%s')) AS ss," \
                 "service_kind AS s, " \
                 "(SELECT ws.service_id, ws.workers_id FROM worker_and_service AS ws WHERE ws.workers_id IN " \
                 "(SELECT workers_message.workers_id FROM workers_message WHERE workers_message.`姓名`='%s')) AS wss" \
                 " WHERE a.area_id = ss.area_id AND wm.workers_id = ss.workers_id " \
                 "AND wss.service_id=s.service_kind_id" % (name, name)

    sql = "SELECT w.id, w.姓名, w.电话, s.详情, a.province, a.city, a.county " \
          "FROM workers AS w, workers_area AS wa, workers_service AS ws, area AS a, service AS s " \
          "WHERE wa.workers_id=w.id AND ws.workers_id=w.id AND a.id=wa.area_id " \
          "AND s.id=ws.service_id AND w.姓名='%s' " % name

    return sql


def match_workers_from_service_area(area, service):
    #    area = "a.province LIKE '%北京%'"  service = "s.`主类别` LIKE '%家庭维修%'"
    """查询指定地区/类别 合适的师傅"""

    sql = "SELECT w.id, w.姓名, w.电话, a.province, a.city, a.county, s.详情 " \
          "FROM workers AS w, workers_area AS wa, workers_service AS ws, area AS a, service AS s " \
          "WHERE s.id=ws.service_id AND a.id=wa.area_id AND w.id=wa.workers_id AND w.id=wa.workers_id " \
          "AND %s AND %s GROUP BY w.id" % (area, service)

    return sql


def get_data(sql):
    conn = pymysql.connect(host="192.168.1.103",
                           user="root",
                           password="root",
                           database="premetheus",
                           port=3306,
                           charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    if cur.rowcount == 0:
        print("匹配失败")
    else:
        result = cur.fetchall()
        result = list(list(i) for i in result)
    cur.close()
    print('end')
    conn.close()
    return result


string = 'a.county="%s"' % '东城区'
string = 'a.province="%s"' % '北京市'

# string1 = 's.主类别="%s"' % '家庭维修'
#
# string = 'wa.workers_id=%d' % 1


# area = "a.province='%s'" % '北京市'
# service = "s.`主类别`='%s'" % '家庭维修'

# string = "a.province like '%北京%' "

# string = "s.类目 LIKE '%房屋维修%'"
# sql = match_workers_from_service_area(area, service)
# # sql = get_worker_from_service_area(area, service)
# get_data(sql)


class Work :
    def __init__(self, id, name, tel) :
        self.id = id
        self.name = name 
        self.tel = tel

class WorkDao :
    def queryByName(self, name) :
        sql = 'SELECT id,姓名,电话,身份证号 FROM workers WHERE 姓名 LIKE "%' + name + '%"'
        list = get_data(sql)
        return list
    def queryByArea(self, areaName) :
        area_id_list = 'SELECT id FROM area WHERE areaName = ' + areaName  
        # area_id_list = []
        # for area in area_list :
        #     area_id_list.append(area.id)
        ## SELECT * FROM workers_area WHERE area_id IN (area_id_)
        work_id_list
        # SELECT * FROM workers WHERE id IN (work_id_list)

    def queryByParams(name, tel, address) :
        sql = 'SELECT * FROM workers'
        # if 
        if name not is None :
            sql = sql + 'WHERE name = ' + name
        if tel not is None :
            sql = 

def search_work_info(request) :
    name = request.GET.get('work_name')
    print('-----http 接收到页面的师傅名字 : ' + name)
    result = {}
    try :
        workDao = WorkDao()
        result_list = []
        data = workDao.queryByName(name)
        for work in data :
            work_json = parse_array_to_json(work)
            result_list.append(work_json)
    except Exception as e:
        print('后端异常' + str(e))
        result['status'] = 1
        result['errMsg'] = '数据库查询异常'
        return JsonResponse(result)
    result['status'] = 0
    # result['data'] = [{'id': 1, 'name':'小马','tel':111, 'skill' :"技能"}]
    result['data'] = result_list
    print("处理成功，返回参数:" + str(result))
    return JsonResponse(result)

def parse_array_to_json(list) : 
    map = {}
    for work in list :
        map['id'] = list[0]
        map['name'] = list[1]
        map['tel'] = list[2]
        map['skill'] = list[3]
    return map


def searchWorker(request) :
    name = request.GET.get('name')
    ## 查询工人信息
    worker_list = []
    