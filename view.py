# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 11:10:50 2015

@author: kentarokira
"""

from dbio import dbiomaker

def view():
    bukkens=[]
    # 物件情報のDBIOインスタンスを作成
    dbio = dbiomaker()
    bukkens=dbio.select()
    return bukkens