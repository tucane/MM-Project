import os
import sys
module_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(module_dir, '../data_utils/'))

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from utils import fill_empty_data, getRValue

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

    def train(self, data, labels, path):
        if not self.regressor:
            self.regressor = RandomForestRegressor()

        self.regressor.fit(data, labels)

        joblib.dump(self.regressor, path)

    def predict(self, building_data):
        return self.regressor.predict(building_data)


def form_to_data(form):
    building_volume = form['building_volume'].data
    date = form["date"].data
    building_type = form["building_type"].data
    set_temp = form["set_temp"].data
    rad_norm = form["rad_norm"].data
    rad_hor = form["rad_hor"].data
    out_temp = form["out_temp"].data
    location = form['location'].data
    humidity = form['humidity'].data

    #use date.timetuple().tm_yday if combine both month and day to a single number
    #TODO: get the R_VAL dependency correct
    result = np.array([[building_volume, date.month, date.day, 0, getRValue(), set_temp, rad_norm, rad_hor, out_temp, humidity]])

    return result

def file_to_data(df):
    #TOFIX:
    df['RValue'] = df.apply(lambda x: getRValue(), axis=1)

    df = df.filter(items=[df.columns[1], df.columns[2], df.columns[3], df.columns[4], df.columns[5], 'RValue', df.columns[6],
                          df.columns[7], df.columns[8], df.columns[11]])

    #fill in the data that are missing
    fill_empty_data(df)

    #it's possible that the entire column is missing. Replace it with 0 in that case
    df.fillna(0, inplace=True)

    return df.values

