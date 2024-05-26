import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app
bootstrap = Bootstrap(app)
login_manager = LoginManager(app) # 实例化扩展类

### 初始化Flask-Lgoin，用于记录当前用户的用户模型类
@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象

login_manager.login_view = 'login' # 视图保护，重定向至login页面

###templates模版上下文处理函数, 把用户注册进上下文
@app.context_processor
def inject_user(): # 函数名可以随意修改
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user) # 需要返回字典，等同于 return {'user': user}

### 使用CSRFProtect实现CSRF保护
csrf = CSRFProtect()
csrf.init_app(app)


from watchlist import views, errors, commands