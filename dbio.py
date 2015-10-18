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

#from sqlalchemy.ext.declarative import declarative_base
# SQLAlchemyお決まりの処理
#Base = declarative_base()

if os.uname()[1] == "kira-no-MacBook-Air.local":
    url = 'postgresql://pybv:pybv@localhost:5432/pybv_db'
else:    
    #urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
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
    Column("info",String)
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
    
    def __repr__(self):
        return "<BukkenInfo(%s,%s)>" % (self.website,self.name)

class dbiomaker():        
    def insert(self,bukkens):
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            l = session.query(BukkenInfo).first() 
            print(l)
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
            for bukken in bukkens:
                print(bukken)
        except exc.SQLAlchemyError as e:
            print("--error--")
            print(e.with_traceback)
            session.rollback()
        finally:
            print("--finally--")
            session.close()
        return bukkens
            

#テーブルとDBIOクラスの関連付け
mapper(BukkenInfo,bukken_info_table)


            
