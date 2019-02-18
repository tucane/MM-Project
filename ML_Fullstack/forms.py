from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, DecimalField, IntegerField, SubmitField, FileField, validators, StringField

class BuildingForm(FlaskForm):
    building_name = StringField('building_name')
    building_volume = DecimalField('building_volume')
    date = DateField('date')
    building_type = SelectField('building_type', choices=[("Glass", "Glass"),
                                                          ("Steel", "Steel"),
                                                          ("Concrete", "Concrete"),
                                                          ("Wood", "Wood")])

    set_temp = DecimalField('set_temp')
    rad_norm = IntegerField('rad_norm')
    rad_hor = IntegerField('rad_hor')
    location = StringField('location')
    out_temp = DecimalField('out_temp')
    humidity = DecimalField('humidity')
    estimate = SubmitField('estimate')
    input_file = FileField('input_file', [validators.Optional()])
