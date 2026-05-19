from flask_wtf import FlaskForm
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField("Job Title")
    team_leader = IntegerField("Team Leader id", validators=[DataRequired()])
    work_size = IntegerField("Work Size")
    collaborators = StringField("Collaborators")
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField("Submit")
