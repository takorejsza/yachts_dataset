from flask import redirect, render_template, flash
from app import app
from app.forms import EstimatorForm
import pickle
import numpy as np
import datetime
import joblib
import warnings

warnings.filterwarnings('ignore')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EstimatorForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():

        condition = {'Poor':0, 'Fair':0, 'Good':0, 'Excellent':0}
        condition[form.condition.data] = 1

        rigging = {
            'Cruiser':0, 'Cutter':0, 'Day Sailer':0, 'Ketch':0, 'Sloop':0
        }
        rigging[form.rigging.data] = 1

        year = int(datetime.datetime.today().year)

        features = [
            form.length.data,
            form.year.data,
            form.beam.data,
            form.draft.data,
            form.hull_type.data,
            form.engine_type.data,
            form.no_engines.data,
            form.engine_pos.data,
            form.no_cabins.data,
            year,
            form.hull_material.data,
            rigging['Cruiser'],
            rigging['Day Sailer'],
            rigging['Sloop'],
            rigging['Cutter'],
            rigging['Ketch'],
            condition['Excellent'],
            condition['Fair'],
            condition['Good'],
            condition['Poor']
        ]

        vals = np.array(features).reshape(1,len(features))
        
        with open(r"models/regression_model.compressed", 'rb') as file:
            model = joblib.load(file) # pickle.load(file)
            print(model.predict(vals))
            prediction = max(round(model.predict(vals)[0],0), 5e3)

        form.estimate = "${:,.0f}".format(prediction)
        return render_template('index.html', title='Estimate', form=form)
    return render_template('index.html', title='Estimate', form=form)
