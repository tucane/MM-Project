from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, DecimalField, IntegerField, SubmitField

class BuildingForm(FlaskForm):
    date = DateField("date")
    building_type = SelectField("building_type", choices=[("Glass", "Glass"), ("Concrete", "Concrete"), ("Steel", "Steel"), ("Wood", "Wood")])

    set_temp = DecimalField('set_temp')
    irradiation_norm = IntegerField('rad_norm')
    irradiation_hor = IntegerField('rad_hor')
    out_temp = DecimalField('out_temp')
    estimate = SubmitField('estimate')