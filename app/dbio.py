# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 11:12:07 2015

@author: kentarokira
"""
from sqlalchemy import Table,Column,Integer,String,MetaData,create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc #例外処理
import os
import re
from datetime import datetime

#from sqlalchemy.ext.declarative import declarative_base
# SQLAlchemyお決まりの処理
#Base = declarative_base()

if "DATABASE_URL" in os.environ.keys():
    url = os.environ["DATABASE_URL"]
elif os.uname()[1] == "kira-no-MacBook-Air.local":
    url = 'postgresql://pybv:pybv@localhost:5432/pybv_db'
else:
    url = 'postgresql://postgres@localhost:5432/pybv_db'
engine = create_engine(url, echo=False)     
     
# テーブル作成
metadata = MetaData()
bukken_info_table = Table("bukken_info",metadata,
    Column("id",Integer,primary_key=True),
    #サイト名
    Column("website",String),
    #サイトURL
    Column("websiteURL",String),
    #物件名称
    Column("name",String),
    #物件名称
    Column("link",String),
    #画像パス
    Column("photoURL",String),
    #家賃
    Column("yatin",String),
    #最寄駅
    Column("eki",String),
    #間取り
    Column("madori",String),
    #コメント
    Column("info",String),
    #検索用家賃
    Column("yatin_select",Integer),
    #検索用家賃
    Column("updatetime",String)
)
metadata.create_all(engine)

#DBIO
class BukkenInfo():
    def __init__(self, website, websiteURL, name, link, photoURL, yatin, eki, madori, info):
        #サイト名
        self.website=website
        #サイトURL
        self.websiteURL=websiteURL
        #物件名称
        self.name=name
        #物件リンク
        self.link=link
        #画像パス
        self.photoURL=photoURL
        #家賃
        self.yatin=yatin
        #最寄駅
        self.eki=eki
        #間取り
        self.madori=madori
        #コメント
        self.info=info
        #検索用家賃
        self.yatin_select=re.findall(r'[0-9]+', yatin.replace(',', ''))[0]
        #更新日
        self.updatetime=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
    def __repr__(self):
        return "<BukkenInfo(%s,%s)>" % (self.website,self.name)

class dbiomaker():        
    def insert(self,bukkens):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            print("--try--")
            for bukken in bukkens:
                session.add(bukken)
            session.commit()
            print("--commited--")
        except exc.SQLAlchemyError as e:
            print("--error--")
            print(e.with_traceback)
            session.rollback()
        finally:
            print("--finally--")
            session.close()
            
    def select(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        bukkens=[]
        try:
            print("--try--")
            bukkens = session.query(BukkenInfo).all() 
            #for bukken in bukkens:
            #    print(bukken)
        except exc.SQLAlchemyError as e:
            print("--error--")
            print(e.with_traceback)
            session.rollback()
        finally:
            print("--finally--")
            session.close()
        return bukkens
 
    def selectWith(self,select):
        Session = sessionmaker(bind=engine)
        session = Session()
        bukkens=[]
        try:
            print("--try--")
            p=session.query(BukkenInfo)
            if select["website"] != 'ALL':
                p=p.filter(BukkenInfo.website==select["website"])
            if select["eki"] != 'ALL':
                p=p.filter(BukkenInfo.eki.like('%'+select['eki']+'%'))
            if select["madori"] != 'ALL':
                p=p.filter(BukkenInfo.madori.like('%'+select['madori']+'%'))
            if select["yatin"] != 'ALL':
                yatin=int(select["yatin"])
                p=p.filter(BukkenInfo.yatin_select.between(yatin,yatin+19999))
            bukkens = p.all()
            #for bukken in bukkens:
            #    print(bukken)
        except exc.SQLAlchemyError as e:
            print("--error--")
            print(e.with_traceback)
            session.rollback()
        finally:
            print("--finally--")
            session.close()
        return bukkens

    def deleteBySite(self,webSiteName):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            print("--try--")
            #bukkens = session.query(BukkenInfo).all() 
            #session.delete(bukkens)
            #session.commit()
            session.query(BukkenInfo).filter(BukkenInfo.website==webSiteName).delete()
            session.commit()
        except exc.SQLAlchemyError as e:
            print("--error--")
            print(e.with_traceback)
            session.rollback()
        finally:
            print("--finally--")
            session.close()

         
class BukkenSetter():           
    def getBukkenInfoByDic(self,dic):
        info = BukkenInfo(
        #サイト名
        dic["website"],
        #サイトURL
        dic["websiteURL"],
        #物件名称
        dic["name"],
        #物件名称
        dic["link"],
        #画像パス
        dic["photoURL"],
        #家賃
        dic["yatin"],
        #最寄駅
        dic["eki"],
        #間取り
        dic["madori"],
        #コメント
        dic["info"]
        )
        return info

#テーブルとDBIOクラスの関連付け
mapper(BukkenInfo,bukken_info_table)

if __name__ == '__main__':
    io = dbiomaker()
    io.deleteBySite('good room')
    #a=eval("HTML"+"."+BP+'("'+BC+'")'+BS)
            
