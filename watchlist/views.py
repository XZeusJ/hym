from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db # 导入程序实例和扩展对象
from watchlist.models import User, Movie, RawMaterialCost # 导入模型类
from watchlist.forms import RawMaterialCostForm


###主页路由
# 增加材料条目
@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:  # 如果当前用户未认证
        return redirect(url_for('login'))  # 重定向到主页
    
    form = RawMaterialCostForm()
    #这里的form是一个flask_wtf引入的FlaskForm类，这个类可以被jinja2渲染
    if form.validate_on_submit():
        new_material = RawMaterialCost(
            material_name=form.material_name.data,
            material_specification=form.material_specification.data,
            unit_price_per_g=form.unit_price_per_g.data,
            net_weight=form.net_weight.data,
            gross_weight=form.gross_weight.data,
            product_qualification_rate=form.product_qualification_rate.data,
            to_calculate=form.to_calculate.data
        )
        db.session.add(new_material)
        db.session.commit()
        flash('Item created.') 
        return redirect(url_for('index'))
        
    raw_material_costs = RawMaterialCost.query.all()
    #这里的raw_material_costs是一个flask_sqlalchemy引入的db.Model类，这个类可以被jinja2渲染
    return render_template('index.html', raw_material_costs=raw_material_costs, form = form)

# 编辑材料条目
@app.route('/material/edit_material/<int:material_id>', methods=['GET', 'POST'])
@login_required
def edit_material(material_id):
    form = RawMaterialCostForm()
    material = RawMaterialCost.query.get_or_404(material_id)
    if not material:
        return 'Material not found', 404
    if form.validate_on_submit(): # 处理编辑表单的提交请求
        material.material_name = form.material_name.data
        material.material_specification = form.material_specification.data
        material.unit_price_per_g = form.unit_price_per_g.data
        material.net_weight = form.net_weight.data
        material.gross_weight = form.gross_weight.data
        material.product_qualification_rate = form.product_qualification_rate.data
        material.to_calculate = form.to_calculate.data
        
        db.session.commit()
        flash('Material updated.')
        return redirect(url_for('index'))
    #给form模型对象的值赋给表单字段，用于在表单上预填充数据，例如在编辑页面上显示现有记录的值，以便用户可以看到并修改它们。
    form.material_name.data = material.material_name
    form.material_specification.data = material.material_specification
    form.unit_price_per_g.data = material.unit_price_per_g
    form.net_weight.data = material.net_weight
    form.gross_weight.data = material.gross_weight
    form.product_qualification_rate.data = material.product_qualification_rate
    form.to_calculate.data = material.to_calculate
    return render_template('edit.html', form=form)  # 传入被编辑的记录

# 删除材料条目
@app.route('/material/delete_material/<int:material_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required # 登陆保护
def delete_material(material_id):
    material = RawMaterialCost.query.get_or_404(material_id)
    db.session.delete(material)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Material deleted.')
    return redirect(url_for('index'))

# 计算总费用
@app.route('/costs')
def costs():
    # 在视图函数中计算总和
    materials = RawMaterialCost.query.filter(RawMaterialCost.to_calculate == True).all()
    total_ttl = sum(material.unit_price_per_g * (material.net_weight + material.gross_weight) / material.product_qualification_rate
                for material in materials if material.to_calculate)
    return render_template('costs.html', materials = materials, total_ttl=total_ttl)

# 用户登陆
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')

### 用户登出
@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('login'))  # 重定向回首页

### 用户设置名字
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')
