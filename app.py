# -*- coding: utf-8 -*-

from bottle import route, run, request
from bottle import TEMPLATE_PATH, jinja2_template as template
import scraping
import view
import os

#templateパスの追加
TEMPLATE_PATH.append("./views")

@route('/update')
def update():
    scraping.update()
    return template('save.j2')
    
@route('/')
def index():
    return template('index.j2')

@route('/login', method='POST')
def search():
    website = request.forms.get('website')
    price = request.forms.get('price')
    madori = request.forms.get('madori')
    eki = request.forms.get('eki')
    print(website)
    print(price)
    print(madori)
    print(eki)
    select={"website":website,"price":price,"madori":madori,"eki":eki}
    bukkens=view.viewSelect(select)
    return template('bukken.j2', bukkens=bukkens)

@route('/show')
def show():
    bukkens=view.viewALL()
    return template('bukken.j2', bukkens=bukkens)
    
run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

#if __name__ == '__main__':
