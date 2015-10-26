# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 11:11:55 2015

@author: kentarokira
"""

from selenium import webdriver
import lxml.html
import lxml.cssselect
import os
#from dbio import BukkenInfo
from dbio import dbiomaker, BukkenSetter
import yaml as yamllib
    
def update():
    print("---start update---")
    #新規取得した物件情報を格納
    bukkens=[]
    # 物件情報のDBIOインスタンスを作成
    dbio = dbiomaker()

    #linea start
    #yamlデータ取得    
    f = open("xpath/"+"linea.yaml", 'r')
    yaml = yamllib.load(f)  # 読み込む
    f.close() 
    # URL_PRE + ページ番号 + URL_POST　でURLを構成する
    URL_LINEA_PRE = 'http://www.linea.co.jp/article/list/pgnum/'
    URL_LINEA_POST = '/type/rent/pre2/1/'
    #  物件サイトから情報を取得
    for i in range(1,2):
        url = URL_LINEA_PRE + str(i) + URL_LINEA_POST
        print("---getting from "+ url +"---")
        bukkens.extend(getBukkensFromYamlInPage(yaml,url))
    #物件情報削除
    dbio.deleteBySite(yaml["website"])
    #linea end

    #Rstore start
    #yamlデータ取得    
    f = open("xpath/"+"Rstore.yaml", 'r')
    yaml = yamllib.load(f)  # 読み込む
    f.close() 
    URL_RSTORE_PRE = 'http://www.r-store.jp/newarrival/'
    URL_RSTORE_RSTORE = '?odr=5&num=50'
    #  物件サイトから情報を取得
    for i in range(1,2):
        url = URL_RSTORE_PRE + str(i) + URL_RSTORE_RSTORE
        print("---getting from "+ url +"---")
        bukkens.extend(getBukkensFromYamlInPage(yaml,url))
    #物件情報削除
    dbio.deleteBySite(yaml["website"])
    #Rstore end
    
    
    #good room start
    #yamlデータ取得    
    f = open("xpath/"+"goodroom.yaml", 'r')
    yaml = yamllib.load(f)  # 読み込む
    f.close()
    URL_GOODROOM_PRE = 'http://www.goodrooms.jp/sch/sch_list.php?page_num=2&sort=&=&sch_flg=&item=0&price=0-99999&b_area=0-99999&eki_walk=0&chikunen=0&rs_price=&madori=0&no_r_price=0&no_s_price=0&cond_money_combo=0&kodawari=0&setsubi_cd=0&g_point1=0&g_point2=0&g_point3=0&g_point4=0&g_point5=0&categoly=0&state=&update=&create_date=&pref_cd=0&word=&canonical_url=/sch/sch_list.php?page_num='
    URL_GOODROOM_RSTORE = ''
    #  物件サイトから情報を取得
    for i in range(1,2):
        url = URL_GOODROOM_PRE + str(i) + URL_GOODROOM_RSTORE
        print("---getting from "+ url +"---")
        bukkens.extend(getBukkensFromYamlInPage(yaml,url))
    #物件情報削除
    dbio.deleteBySite(yaml["website"])
    #good room end
    #️DBへ格納
    dbio.insert(bukkens)
    print("---end update---")

def getBukkensFromYamlInPage(yaml,pageUrl):
    
    # webサイトから取得した物件リストを格納
    bukkens = []

    #開発環境と本番環境でPhantomJSの呼び出し方が異なるため、ホスト名で振り分け
    if os.uname()[1] == "kira-no-MacBook-Air.local":
        driver = webdriver.PhantomJS(executable_path='/Applications/phantomjs-1.9.2-macosx/bin/phantomjs')
    else:    
        driver = webdriver.PhantomJS()
    #webサイトからデータ取得
    driver.get(pageUrl)
    #HTMLは未使用にみえるが、文字列指定の形でevalで使用している
    HTML = lxml.html.fromstring(driver.page_source)
    
    #登録用物件辞書
    bukkenDic={}
    bukkenSetter=BukkenSetter()
    
    #mainルーチン
    # g is GROUP
    # u is UNIT
    # pcs is UNIT item
    #共通情報設定
    yamlid="website"
    bukkenDic.update({yamlid:yaml[yamlid]})
    yamlid="websiteURL"
    bukkenDic.update({yamlid:yaml[yamlid]})
    #print("G1 --YAML[GROUPS] => YAML[GROUP]--:YAMLファイルからGROUPの検索条件を取得")
    for g in yaml:
        if g == "GROUP":
            gp = yaml[g]["PROTOCOL"]
            gc = yaml[g]["COMMAND"]
            gs = yaml[g]["SELECTOR"]
            #print("G2 --YAML[GROUP] => HTML[GROUPS]--:GROUP検索条件よりHTMLのGROUP群を抽出")        
            groups=eval("HTML"+"."+gp+'("'+gc+'")'+gs)
            #print("G3 --HTML[GROUPS] => HTML[GROUP]--:HTMLのGROUP群を１つづつループ処理")
            for group in groups:
                #print("U1 --YAML[GROUP] => YAML[UNIT]--:YAMLファイルからUNITの検索条件を取得")
                for u in yaml[g]:
                    if u == "UNIT":
                        up = yaml[g][u]["PROTOCOL"]
                        uc = yaml[g][u]["COMMAND"]
                        us = yaml[g][u]["SELECTOR"]
                        #print("U2 --YAML[UNIT] => HTML[UNITS]--:UNIT検索条件よりHTMLのUNIT群を抽出")
                        #<div class="article-box clearfix">
                        units=eval("group"+"."+up+'("'+uc+'")'+us)
                        #print("U3 --HTML[UNITS] => HTML[UNIT]--:HTMLのUNIT群を１つづつループ処理")
                        for unit in units:
                            #print("UI1--YAML[UNIT] => YAML[UNITITEMS]--:YAMLファイルからUNITITEM群の検索条件を取得")
                            for uis in yaml[g][u]:
                                if uis =="UNITITEMS":
                                    #print("UI2--YAML[UNITITEMS] => YAML[UNITITEM]--:YAMLファイルからUNITITEMの検索条件を取得")
                                    for ui in yaml[g][u][uis] :
                                        if ui != "IGNORE":
                                            p = yaml[g][u][uis][ui]["PROTOCOL"]
                                            c = yaml[g][u][uis][ui]["COMMAND"]
                                            s = yaml[g][u][uis][ui]["SELECTOR"]
                                            h = yaml[g][u][uis][ui]["HEADER"]
                                            #print("UI3 --YAML[UNITITEM] => HTML[UNITITEM]--:UNITITEM検索条件よりHTMLのUNITITEM情報を抽出")
                                            #print(ui+":"+htmlItemSelector(unit,p,c,s))
                                            #登録用物件辞書に追加
                                            bukkenDic.update({ui:htmlItemSelector(unit,p,c,s,h)})
                                    #物件情報設定
                                    bukkeninfo = bukkenSetter.getBukkenInfoByDic(bukkenDic)
                                    bukkens.append(bukkeninfo)
    return bukkens
        
def htmlItemSelector(HTML,p,c,s,h):
    info = ""
    #メッソドのアクセサ確認　空白、リスト指定[]　は対象外
    if not s=="" and not s.startswith('.') and not s.startswith('['):
        s = "."+ s
        
    #WEBサイトから情報取得
    search=eval("HTML"+"."+p+'("'+c+'")')
    #取得結果毎に抽出方法選択
    #検索結果がない場合
    if len(search) == 0:
        info = "-"
    #検索結果が1件の場合
    elif len(search) == 1:
        #エレメントツリー(ElementTree)に対してテキストを取得する場合は直列化が必要
        #１件のリストに対して[0]でアクセスしてない場合、yaml側のミスの可能性が高い
        #そのため下記の対応を実施
        #if isinstance(search, etree.Element) and not s.startswith('[0]'):
        #    info=lxml.html.tostring(search, method='text')
        if isinstance(search, list) :
            if s == ".all":
                info = search[0].text_content()
            elif not s.startswith('[0]'):
                info = h + eval("search"+"[0]"+s)   
            else:
                info = h + eval("search"+s)
        else:
            info = h + eval("search"+s)
        
    #それ以外　リストで要素が複数ある場合
    else :
        for li in search:
            lia = eval("li"+s)
            if info == "" :
                info = h + lia
            else:
                info = info + "," + h + lia
    return info

if __name__ == '__main__':

    update()
    #a=eval("HTML"+"."+BP+'("'+BC+'")'+BS)
