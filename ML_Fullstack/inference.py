import os
import sys
module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, '../data_utils/'))

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from data_utils.data_utils import fill_empty_data, getRValue, get_between_dates

class Model:

    def __init__(self, weights_path=None):
        self.regressor = None
        if weights_path:
            self.load_weights(weights_path)

    def load_weights(self, weights_path):
        try:
            with open(weights_path) as fp:
                self.regressor = joblib.load(weights_path)

        except IOError:
            print(weights_path + " does not exist")

    #change for different training algorithm/hyperparameters
    def train(self, data, labels, path):
        if not self.regressor:
            self.regressor = RandomForestRegressor()

        self.regressor.fit(data, labels)

        joblib.dump(self.regressor, path)

    def predict(self, building_data):
        return self.regressor.predict(building_data)

#convert the regular input fields to data used by the ML model
def form_to_data(form):
    building_volume = form['building_volume'].data
    from_date = form["from_date"].data
    to_date = form['to_date'].data
    building_type = form["building_type"].data
    set_temp = form["set_temp"].data
    rad_norm = form["rad_norm"].data
    rad_hor = form["rad_hor"].data
    out_temp = form["out_temp"].data
    location = form['location'].data
    humidity = form['humidity'].data

    #use date.timetuple().tm_yday if combine both month and day to a single number

    result = []
    days = get_between_dates(from_date, to_date)
    for day in days:
        for hour in range(24):
            result.append([building_volume, day.month, day.day, hour, getRValue(building_type), set_temp, rad_norm, rad_hor, out_temp, humidity])

    result = np.array(result)

    return result

#convert the comparative input fields to data used by the ML model
def comparative_form_to_data(form):
    building_volume = form['building_volume'].data
    building_volume2 = form['building_volume2'].data
    from_date = form["from_date"].data
    to_date = form['to_date'].data
    building_type = form["building_type"].data
    building_type2 = form['building_type2'].data
    set_temp = form["set_temp"].data
    set_temp2 = form['set_temp2'].data

    rad_norm = form["rad_norm"].data
    rad_hor = form["rad_hor"].data

    out_temp = form["out_temp"].data
    location = form['location'].data
    humidity = form['humidity'].data
    humidity2 = form['humidity2'].data

    result1 = []
    result2 = []
    days = get_between_dates(from_date, to_date)

    for day in days:
        for hour in range(24):
            result1.append([building_volume, day.month, day.day, hour, getRValue(building_type), set_temp, rad_norm, rad_hor,
                            out_temp, humidity])

            result2.append([building_volume2, day.month, day.day, hour, getRValue(building_type2), set_temp2, rad_norm, rad_hor,
                            out_temp, humidity2])

    result1 = np.array(result1)
    result2 = np.array(result2)

    return result1, result2

#convert the uploaded csv file to data used by the ML model
def file_to_data(df):
    #get R value from the building type
    df['RValue'] = df.apply(lambda x: getRValue(x[df.columns[2]]), axis=1)

    df = df.filter(items=[df.columns[1], df.columns[3], df.columns[4], df.columns[5], df.columns[6], 'RValue', df.columns[7],
                          df.columns[8], df.columns[9], df.columns[11]])

    #fill in the data that are missing
    fill_empty_data(df)

    #it's possible that the entire column is missing. Replace it with 0 in that case
    df.fillna(0, inplace=True)

    return df.values

