# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 11:11:55 2015

@author: kentarokira
"""

from selenium import webdriver
import lxml.html
import os
#from dbio import BukkenInfo
from dbio import dbiomaker, BukkenInfo

def update():
    print("---start update---")
    # URL_PRE + ページ番号 + URL_POST　でURLを構成する
    URL_PRE = 'http://www.linea.co.jp/article/list/pgnum/'
    URL_POST = '/type/rent/pre2/1/'
    # 複数サイトの物件情報を格納
    bukkens=[]
    #  物件サイトから情報を取得
    for i in range(1,2):
        url = URL_PRE + str(i) + URL_POST
        print("---getting from "+ url +"---")
        bukkens.extend(getFromPage(url))

    # 物件情報のDBIOインスタンスを作成
    dbio = dbiomaker()
    #️DBへ格納
    dbio.insert(bukkens)
    print("---end update---")
    
def getFromPage(url):
    print("--- start getFromPage---")
    #開発環境と本番環境でPhantomJSの呼び出し方が異なるため、ホスト名で振り分け
    if os.uname()[1] == "kira-no-MacBook-Air.local":
        driver = webdriver.PhantomJS(executable_path='/Applications/phantomjs-1.9.2-macosx/bin/phantomjs')
    else:    
        driver = webdriver.PhantomJS()
    driver.get(url)

    SITE_ROOT='https://www.linea.co.jp'
    bukkens = []

    root = lxml.html.fromstring(driver.page_source)
    links = root.xpath("//div[@class='article-box clearfix']")
    for link in links:
        for anchor in link.xpath("descendant::a"):
            if anchor.text != None :
                #画像設定
                imglist = []
                imgElement = link.xpath("descendant::div[@class='article-photo clearfix']//img")[0].attrib['src']
                if imgElement == None:
                    imglist.append("")
                else:
                    imglist.append(SITE_ROOT+imgElement)
                #家賃
                yatins = link.xpath("descendant::li[@class='price']")
                if len(yatins) == 0:
                    yatin = "-"
                else:
                    yatin = yatins[0].text
                #最寄駅
                eki=""
                for ekis in link.xpath("descendant::li[@class='area']"):
                    eki = eki + "/" + ekis.text
                #間取り
                madoris = link.xpath("descendant::li[@class='layout']")
                if len(madoris) == 0:
                    madori = "-"
                else:
                    madori = madoris[0].text
                #
                infos = link.xpath("descendant::div[@class='article-info']//p[@class='info-txt']")
                if len(infos) == 0:
                    info = "-"
                else:
                    info = infos[0].text
                #物件情報設定
                bukkeninfo = BukkenInfo(
                    "linea",
                    SITE_ROOT,
                    anchor.text, 
                    anchor.attrib['href'],
                    imglist[0],
                    yatin,
                    eki,
                    madori,
                    info
                )
                print(bukkeninfo.__repr__)
                bukkens.append(bukkeninfo)
                #print(anchor.text + " , " +anchor.attrib['href'] +" , "+imglist[0])
    return bukkens

if __name__ == '__main__':
    update()