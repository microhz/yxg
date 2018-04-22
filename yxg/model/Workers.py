# -*- coding:utf-8 -*-
## 与workers表对应的
class Workers :
    def __init__(self, ** args) :
        self.id = args.get('id') 
        self.name = args.get('name')
        self.tel = args.get('tel')
        self.address = args.get('address')