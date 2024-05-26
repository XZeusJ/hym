from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class RawMaterialCostForm(FlaskForm):
    material_name = StringField('Material Name', validators=[DataRequired()])
    material_specification = StringField('Material Specification', validators=[DataRequired()])
    unit_price_per_g = FloatField('Unit Price per g', validators=[DataRequired()])
    net_weight = FloatField('Net Weight', validators=[DataRequired()])
    gross_weight = FloatField('Gross Weight', validators=[DataRequired()])
    product_qualification_rate = FloatField('Product Qualification Rate', validators=[DataRequired()])
    to_calculate = BooleanField('Calculate?')
    submit = SubmitField('Submit')