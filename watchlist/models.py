from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


### 数据库用户表
# class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
class User(db.Model, UserMixin): #UserMixin的属性用于判断当前用户的认证状态
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字(昵称)
    username = db.Column(db.String(20))  # 用户名(账号)
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值



### 数据库电影表
class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

### 原材料费用表
class RawMaterialCost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String(100))  # 材料名称
    material_specification = db.Column(db.String(100))  # 材料规格
    unit_price_per_g = db.Column(db.Float)  # 单价/g
    net_weight = db.Column(db.Float)  # 材料净重
    gross_weight = db.Column(db.Float)  # 材料毛边
    product_qualification_rate = db.Column(db.Float)  # 产品合格率
    to_calculate = db.Column(db.Boolean, default=False)  # 判断是否拿到前台进行计算

    