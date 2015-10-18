# -*- coding: utf-8 -*-

from bottle import route, run
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
def show():
    bukkens=view.view()
    return template('bukken.j2', bukkens=bukkens)
    
run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
