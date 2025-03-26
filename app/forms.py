from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class TrainingInputForm(FlaskForm):
    exercise = StringField('種目', validators=[DataRequired()])
    weight = FloatField('重量 (kg)', validators=[DataRequired(), NumberRange(min=0)])
    reps = IntegerField('レップ数', validators=[DataRequired(), NumberRange(min=1)])
    sets = IntegerField('セット数', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('記録する')