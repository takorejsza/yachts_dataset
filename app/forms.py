from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class EstimatorForm(FlaskForm):
    year = IntegerField('Year Manufactured', validators=[DataRequired()])
    
    length = DecimalField('Overall Length', validators=[DataRequired()])
    beam = DecimalField('Beam', validators=[DataRequired()])
    draft = DecimalField('Draft', validators=[DataRequired()])
    
    no_engines = IntegerField('Number of Engines', validators=[DataRequired()])
    
    engine_pos = SelectField('Engine Position', choices=[(0, 'Inboard'), (1, 'Outboard')], coerce=int)
    engine_type = SelectField('Engine Type', choices=[(0, 'Diesel'), (1, 'Gas')], coerce=int) #, validators=v)
    hull_type = SelectField('Hull Type', choices=[(0, 'Mono-Hull'), (1, 'Catamaran')], coerce=int) #, validators=v)
    
    get_estimate = SubmitField('Enter')

    estimate = None
    