import os
import sys
module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, '../data_utils/'))

from flask import render_template, request, make_response, redirect, url_for, session, flash
from .forms import BuildingForm, ComparativeBuildingForm
from .inference import Model, file_to_data, form_to_data
import numpy as np
import pandas as pd
from data_utils.data_utils import generate_table, plot_daily
from . import app


model = Model(os.path.join(module_dir, 'weights/default_weights.joblib'))

@app.route('/')
def index():
    form = BuildingForm()
    return render_template('index.html', form=form)

@app.route('/prediction', methods = ['POST'])
def prediction():
    form = BuildingForm()
    if request.method == 'POST':

        #if the user opt to use the comparative fields
        if form['compare'].data:
            return redirect(url_for('comparative_input'))

        #data from file
        if form['input_file'].data:
            input_file = request.files['input_file']
            df = pd.read_csv(input_file, header=0)
            building_data = file_to_data(df)
            values = model.predict(building_data).round(decimals=2)
            return generate_outfile(values, df)


        #data from form
        elif form.validate():
            building_data = form_to_data(form)
            result = model.predict(building_data)

            num_days = result.shape[0] // 24
            #sum up the hours
            result = np.sum(result.reshape(24, num_days, 2), axis=0)


            #for plottint
            days = ["{}/{}".format(d[1], d[2]) for d in building_data[::24]]    #take a data per 24 datapoints to represent day
            heating_data = result[:, 0]
            cooling_data = result[:, 1]

            heating_plt, cooling_plt, heating_cum_plt, cooling_cum_plt = plot_daily(days, heating_data, cooling_data)

            display = generate_table(result, form)

            return render_template('prediction.html', value=display, plot1=heating_plt, plot2=cooling_plt, plot3=heating_cum_plt, plot4=cooling_cum_plt)

        #invalid
        else:
            flash('File or input fields must contain valid data')
            return redirect(url_for('index'))

@app.route('/compare-fields')
def comparative_input():
    form = ComparativeBuildingForm()
    return render_template('compare.html', form=form)

@app.route('/prediction-comparative', methods = ['POST'])
def comparative_predict():
    form = ComparativeBuildingForm()

    if request.method == 'POST':

        #back to the original input
        if form['original'].data:
            return redirect(url_for('index'))

        #produce the comparative prediction
        else:
            return "hello world"

@app.route('/downloads/')
def file_downloads():
    return render_template('downloads.html')

@app.route('/downloads/outputs.csv')
def get_file():
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