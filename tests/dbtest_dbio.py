# -*- coding:utf-8 -*-
import bottle
import sqlalchemy
import sqlalchemy.ext.declarative
# SQLAlchemyお決まりの処理
Base = sqlalchemy.ext.declarative.declarative_base()
url = 'postgresql://pybv:pybv@localhost:5432/pybv_db'
engine = sqlalchemy.create_engine(url, echo=False)
# sqlalchemyプラグインの設定
app = bottle.Bottle()
plugin = bottle.ext.sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create=False,
    commit=True,
    use_kwargs=False
)
app.install(plugin)
# studentsテーブルの定義
class Student(Base):
    __tablename__ = 'students'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(20))
    kana = sqlalchemy.Column(sqlalchemy.String(40))
@app.get('/show')
def show(db):
    # 登録されている名前を表示
    html = ''
    for student in db.query(Student).all():
        html += student.name + u'<br/>'
    
    return html
# サーバー起動
app.run(host='localhost', port=5000, debug=True)
