# -*- coding:utf-8 -*-
import json

def success_result(data = None) :
    return result(isSuccess = True, data = data)

def fail_result(msg) :
    return result(isSuccess = False, msg = msg)

def result(** kargs) :
    result = {}
    result['isSuccess'] = kargs.get('isSuccess')
    result['data'] = kargs.get('data')
    result['msg'] = kargs.get('msg')
    return result