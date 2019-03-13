import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import io
import base64

def complete_data(data):
    complete_indices = [1, 5, 6, 7, 8, 10, 11, 12]
    for index in complete_indices:
        #complete missing building size
        #data[data.columns[index]].fillna(data[data.columns[index]].mean(), inplace=True)
        fill_empty_data(data[data.columns[index]])

#framework method for filling in the data
def fill_empty_data(df):
    df.fillna(df.mean(), inplace=True)

    #or implement your own

def getRValue():
    return 100

    #TODO fill in formula

#framework for checking validity of the input data
def validateData():
    pass
    #fill in detail here

def generate_table(data, form):
    #create header
    excluded = ['estimate', 'input_file', 'csrf_token']
    headers = [f.name for f in form if f.id not in excluded]
    headers.extend(['heating_avg', 'cooling_avg'])

    results = [f.data for f in form if f.id not in excluded]

    avg_data = np.mean(data, axis=0).round(decimals=2)
    results.extend(avg_data)

    return [headers, results]

def plot_daily(days, heating, cooling):

    heating_plot_url = plot_day_to_energy(days, heating, "Heating Consumption Trend")

    cooling_plot_url = plot_day_to_energy(days, cooling, "Cooling Consumption Trend")

    return (heating_plot_url, cooling_plot_url)

def plot_day_to_energy(days, energy, title):
    img = io.BytesIO()

    plt.plot(days, energy)
    plt.ylabel("Energy Consumption(unit)")
    plt.xlabel("Day")
    plt.title(title)
    plt.savefig(img, format='png')

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def get_between_dates(from_date, to_date):
    day_between = (to_date - from_date).days + 1    #inclusive

    if day_between <= 0:        #should have to_data after start date
        day_between = 1

    return [from_date + datetime.timedelta(i) for i in range(day_between)]
