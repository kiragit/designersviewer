# -*- coding: utf-8 -*-

from bottle import route, run, request, auth_basic
import hashlib
import base64
from bottle import TEMPLATE_PATH, jinja2_template as template
import scraping
import view
import os
from bottle import static_file

#このスクリプトがあるフォルダの絶対パス
ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) 
#templateパスの追加
TEMPLATE_PATH.append(ROOT_PATH  + "../views")

@route('/js/<filename>')
def js_static(filename):
    return static_file(filename, root='./static/js')


@route('/img/<filename>')
def img_static(filename):
    return static_file(filename, root='./static/img')


@route('/fonts/<filename>')
def fonts_static(filename):
    return static_file(filename, root='./static/fonts')


@route('/css/<filename>')
def css_static(filename):
    return static_file(filename, root='./static/css')

def check(username, password):
    #サーバ側設定値の読み取り
    f = open(ROOT_PATH + '/../config/.htpasswd', 'r')
    auth_check_word = f.readline() # ファイル終端まで全て読んだデータを返す
    f.close()
    #ログイン情報の読み込み
    hs= hashlib.sha1()
    hs.update(password.encode("utf-8"))
    login_word = username + ":{SHA}" + str(base64.b64encode(hs.digest()).decode("utf-8"))
    return auth_check_word.strip() ==login_word.strip() 


@route("/manage")
@auth_basic(check)
def manage():
    return template('manage.j2')

@route('/update')
@auth_basic(check)
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
    select={"website":website,"yatin":price,"madori":madori,"eki":eki}
    bukkens=view.viewSelect(select)
    return template('bukken.j2', bukkens=bukkens)

@route('/show')
def show():
    bukkens=view.viewALL()
    return template('bukken.j2', bukkens=bukkens)
    
run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

#if __name__ == '__main__':
