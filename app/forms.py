from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class EstimatorForm(FlaskForm):
    year = IntegerField('Year Manufactured', validators=[DataRequired()])
    
    length = DecimalField('Overall Length', validators=[DataRequired()])
    beam = DecimalField('Beam', validators=[DataRequired()])
    draft = DecimalField('Draft', validators=[DataRequired()])
    
    no_cabins = IntegerField('Number of Cabins', validators=[DataRequired()])
    
    no_engines = IntegerField('Number of Engines', validators=[DataRequired()])
    engine_pos = SelectField('Engine Position', choices=[(0, 'Inboard'), (1, 'Outboard')], coerce=int)
    engine_type = SelectField('Engine Type', choices=[(0, 'Diesel'), (1, 'Gas')], coerce=int) #, validators=v)

    hull_type = SelectField('Hull Type', choices=[(0, 'Mono-Hull'), (1, 'Catamaran')], coerce=int) #, validators=v)
    hull_material = SelectField('Hull Material', choices=[(1, 'Fiberglass'),(0, 'Other')])
    
    rigging = SelectField('Rigging', choices=[
        'Cruiser', 'Cutter', 'Day Sailer', 'Ketch', 'Sloop'
    ])

    condition = SelectField('Condition', choices=[
        # (0,'Poor'), (1, 'Fair'), (2, 'Good'), (3, 'Excellent')
        'Poor', 'Fair', 'Good', 'Excellent'
    ])

    get_estimate = SubmitField('Enter')

    estimate = None
    