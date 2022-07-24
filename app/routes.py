from flask import redirect, render_template, flash
from app import app
from app.forms import EstimatorForm
import pickle
import numpy as np
import warnings

warnings.filterwarnings('ignore')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EstimatorForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        #features = [form.year.data, form.length.data, form.beam.data, form.draft.data,
        #form.no_engines.data, form.engine_type.data, form.hull_type.data]

        #is_mono = 1 if form.hull_type.data == 'Mono-Hull' else 0
        #is_diesel = 1 if form.engine_type.data == 'Diesel' else 0


        features = [
            form.length.data, form.year.data, 
            form.beam.data, form.draft.data,
            form.hull_type.data, form.engine_type.data,
             form.no_engines.data, form.engine_pos.data
        ]

        vals = np.array(features).reshape(1,len(features))

        with open(r"models/regression_model.pkl", 'rb') as file:
            model = pickle.load(file)
            prediction = max(round(model.predict(vals)[0][0],0), 5e3)

        form.estimate = "${:,.0f}".format(prediction)
        return render_template('index.html', title='Estimate', form=form)
    return render_template('index.html', title='Estimate', form=form)
