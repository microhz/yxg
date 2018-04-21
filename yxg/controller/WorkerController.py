# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import JsonResponse
import sys,os
sys.path.append("./yxg/base")
import base
sys.path.append("./yxg/dao")
print(sys.path)
import WorkersDao

def getWorkerInfoByName(request) :
    ## getParams
    print('getWorkerInfoByName')
    name = request.GET.get('work_name')
    # list = [{'id':1,"name":"周宁","tel":"130xxxxxxx","skill":"aaaa"}]
    if (name == None or name == '') :
        return JsonResponse(base.fail_result("请填写名字"))
    result_list = WorkersDao.getByCondition(name = name)
    return JsonResponse(base.success_result(result_list))


def insertWorker(request) :
    name = request.GET.get('work_name')
    tel = request.GET.get('tel')
    address = request.GET.get('address')
    WorkersDao.insertWorkers(name = name, tel = tel, address = address)
    return JsonResponse(base.success_result())