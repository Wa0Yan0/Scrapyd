from flask_cors import CORS
from flask import Flask
from views import Projects, Logs, Menus
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# 跨域请求处理
CORS(app)

# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@47.102.139.195/scrapyd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.register_blueprint(Projects.pro)
app.register_blueprint(Logs.log)
app.register_blueprint(Menus.menu)


if __name__ == '__main__':
    app.run()
