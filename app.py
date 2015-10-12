# -*- coding: utf-8 -*-

from bottle import route, run
from bottle import TEMPLATE_PATH, jinja2_template as template
from selenium import webdriver
import lxml.html
import os

TEMPLATE_PATH.append("./views")

    
@route('/')
@route('/bukken')
def get_linea_pages():
    # URL_PRE + ページ番号 + URL_POST　でURLを構成する
    URL_PRE = 'http://www.linea.co.jp/article/list/pgnum/'
    URL_POST = '/type/rent/pre2/1/'
    #url = 'http://www.linea.co.jp/article/list/type/new'
    bukkens=[]
    for i in range(1,2):
        url = URL_PRE + str(i) + URL_POST
        bukkens.extend(get_a_linea_page(url))
    return template('bukken.j2', bukkens=bukkens)

def get_a_linea_page(url):
    SITE_ROOT='https://www.linea.co.jp'
    bukkens = []
    driver = webdriver.PhantomJS(executable_path='/Applications/phantomjs-1.9.2-macosx/bin/phantomjs')
    #driver = webdriver.PhantomJS()
    driver.get(url)
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
                bukkens.append({'name':anchor.text, 
                'link':anchor.attrib['href'],
                'photo':imglist[0],
                'yatin':yatin,
                'eki':eki,
                'madori':madori,
                'info':info
                })
                #print(anchor.text + " , " +anchor.attrib['href'] +" , "+imglist[0])
    return bukkens

run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))