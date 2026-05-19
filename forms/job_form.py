from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('Типлидер', validators=[DataRequired()])
    work_size = IntegerField('Объём работы (часы)', validators=[DataRequired()])
    collaborators = StringField('Участники')
    start_date = DateField('Дата начала')
    end_date = DateField('Дата окончания')
    is_finished = BooleanField('Завершена')