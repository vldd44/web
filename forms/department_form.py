from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = IntegerField('Руководитель (ID)', validators=[DataRequired()])
    members = StringField('Участники (через запятую)')
    email = StringField('Email')