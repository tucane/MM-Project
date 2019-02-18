import os
import sys

module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, '../data_utils/'))

from flask import Flask, render_template, request, make_response, redirect, url_for, session, flash
from .forms import BuildingForm
from .inference import Model, file_to_data, form_to_data
import numpy as np
import pandas as pd
from utils import generate_table

app = Flask(__name__)
app.secret_key = 'development key'

model = Model('weights/default_weights.joblib')

def run_app():
    app.run()

@app.route('/')
def index():
    form = BuildingForm()
    return render_template('index.html', form=form)

@app.route('/prediction', methods = ['POST'])
def prediction():
    form = BuildingForm()
    if request.method == 'POST':
        #data from file

        if form['input_file'].data:
            input_file = request.files['input_file']
            df = pd.read_csv(input_file, header=0)
            building_data = file_to_data(df)
            values = model.predict(building_data).round(decimals=2)
            return generate_outfile(values, df)

            #No need to do this on another page?
            #session['value'] = value.round(decimals=2).tolist()
            #return render_template('downloads.html')


        #data from form
        elif form.validate():
            building_data = form_to_data(form)
            result = model.predict(building_data).round(decimals=2)
            display = generate_table(result, form)
            return render_template('prediction.html', value=display)

        #invalid
        else:
            flash('File or input fields must contain valid data')
            #return render_template('index.html', form=form)
            return redirect(url_for('index'))

@app.route('/downloads/')
def file_downloads():
    return render_template('downloads.html')

@app.route('/downloads/outputs.csv')
def get_file():
    #TODO: better way to pass down the array instead of using session
    value = session.get('value', None)

    return generate_outfile(value)


def generate_outfile(result, df):
    #append the original file as reference
    df['Heating'] = result[:, 0]
    df['Cooling'] = result[:, 1]
    csv = df.to_csv(index=False)

    #csv = "Heating,Cooling\n" + "\n".join(map(lambda vs: ",".join(map(str, vs)), result))
    response = make_response(csv)
    cd = 'attachment; filename=results.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response