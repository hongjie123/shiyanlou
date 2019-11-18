from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_restful import Api
# 实例化
app = Flask(__name__)

bootstrap=Bootstrap(app)

api=Api(app)

base_path=os.path.abspath(os.path.dirname(__file__))

#配置数据库路径
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(base_path,"orm.sqlite3")
# app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:123456@localhost/shiyanl"
#请求结束自动提交数据库操作
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True
#flask 1版本之后添加的跟踪修改
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

#设置session时需要加盐加密，给加密添加一个随机的盐值，让加密更加复杂安全
app.config["SECRET_KEY"]="123"

#app加载数据库orm
db=SQLAlchemy(app)

