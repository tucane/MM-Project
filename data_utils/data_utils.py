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

def getRValue(building_type):
    type_to_rVal = {"Glass": 10, "Steel": 50, "Concrete": 100, "Wood": 150}    #filler

    return type_to_rVal[building_type]

    #TODO fill in formula

#framework for checking validity of the input data
def validateData():
    pass
    #fill in detail here

def generate_table(data, form):
    #create header
    excluded = ['estimate', 'input_file', 'csrf_token', 'from_date', 'to_date']
    headers = [f.name for f in form if f.id not in excluded]
    headers.extend(['Day', 'Heating(kWh)', 'Cooling(kWh)'])

    r = np.array([f.data for f in form if f.id not in excluded])
    references = np.repeat(r[np.newaxis, :], data.shape[0], axis=0)

    days = np.array(get_between_dates(form['from_date'].data, form['to_date'].data))
    data_with_days = np.hstack((days[:, np.newaxis], data))

    results = np.hstack((references, data_with_days))    #stack the data together

    #avg_data = np.mean(data, axis=0).round(decimals=2)
    #results.extend(avg_data)
    return [headers, results]

def plot_daily(days, heating, cooling):

    heating_plot_url = plot_day_to_energy(days, heating, "Heating Consumption Trend")
    plt.clf()
    cooling_plot_url = plot_day_to_energy(days, cooling, "Cooling Consumption Trend")
    plt.clf()

    heating_cum_plot_url = plot_cum_day_energy(days, heating, "Heating Consumption Cumulative Trend")
    plt.clf()

    cooling_cum_plot_url = plot_cum_day_energy(days, cooling, "Cooling Consumption Cumulative Trend")
    plt.clf()

    return heating_plot_url, cooling_plot_url, heating_cum_plot_url, cooling_cum_plot_url

def plot_day_to_energy(days, energy, title):
    img = io.BytesIO()

    plt.plot(days, energy)
    plt.ylabel("Energy Consumption(kW)")
    plt.xlabel("Day")
    plt.title(title)
    plt.savefig(img, format='png')

    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

def plot_cum_day_energy(days, energy, title):
    img = io.BytesIO()
    cum_energy = [0] * len(days)
    for i in range(len(days)):
        if i == 0:
            cum_energy[i] = energy[i]
        else:
            cum_energy[i] = energy[i] + cum_energy[i - 1]

    plt.plot(days, cum_energy)
    plt.ylabel("Cumulative Energy Consumption(kW)")
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
