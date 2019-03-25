from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, DecimalField, IntegerField, SubmitField, FileField, validators, StringField

class BuildingForm(FlaskForm):
    building_name = StringField('building_name')
    building_volume = DecimalField('building_volume')
    from_date = DateField('from_date')
    to_date = DateField('to_date')
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
    compare = SubmitField('compare')
    input_file = FileField('input_file', [validators.Optional()])

class ComparativeBuildingForm(FlaskForm):
    building_name = StringField('building_name')
    building_volume = DecimalField('building_volume')
    building_volume2 = DecimalField('building_volume2')
    from_date = DateField('from_date')
    to_date = DateField('to_date')

    building_type = SelectField('building_type', choices=[("Glass", "Glass"),
                                                          ("Steel", "Steel"),
                                                          ("Concrete", "Concrete"),
                                                          ("Wood", "Wood")])
    building_type2 = SelectField('building_type2', choices=[("Glass", "Glass"),
                                                          ("Steel", "Steel"),
                                                          ("Concrete", "Concrete"),
                                                          ("Wood", "Wood")])
    set_temp = DecimalField('set_temp')
    set_temp2 = DecimalField('set_temp2')
    rad_norm = IntegerField('rad_norm')
    rad_hor = IntegerField('rad_hor')
    location = StringField('location')
    estimate = SubmitField('estimate')
    original = SubmitField('original')
