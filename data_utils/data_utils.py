import pandas as pd
import numpy as np
import datetime

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

def get_between_dates(from_date, to_date):
    day_between = (to_date - from_date).days + 1    #inclusive

    return [from_date + datetime.timedelta(i) for i in range(day_between)]
