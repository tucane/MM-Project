import pandas as pd
import numpy as np
import pyodbc
import datetime

driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
if not driver_names:
    raise Exception("No pyodbc driver to connect to database")
cnxn = pyodbc.connect(driver=driver_names[0], host='mm490-building.database.windows.net', database='Building_Data',
                      user='mm490admin', password='DDGLZ490mm')
cursor = cnxn.cursor()

class Feature:
    '''
    DATE = 'Date'
    WEEKDAY = 'Weekday'
    MONTH = 'Month'
    WEEK = 'Week'
    DAY = 'Day'
    HOUR = 'Hour'
    WET_BULB_TEMP = 'Outside Wet-Bulb Temp (F)'
    DRY_BULB_TEMP = 'Outside Dry-Bulb Temp (F)'
    COOLING = 'Total Space Cooling - Kwh'
    HEATING = 'Heating - kWh'
    LIGHTING = 'Lighting End-Use Energy - Kwh'
    '''
    MONTH = 'Month'
    DAY = 'Day'
    HOUR = 'Hour'
    SP = 'SetPoint'
    SN = 'SolarIrradiation_Normal'
    SH = 'SolarIrradiation_Horizontal'
    OUT_TEMP = 'OutsideTemp'


class Output:
    '''
    COOLING = 'Total Space Cooling - Kwh'
    HEATING = 'Heating - kWh'
    LIGHTING = 'Lighting End-Use Energy - Kwh'
    '''
    HEATING = 'HeatingEnergy'
    COOLING = 'CoolingEnergy'


def load_data_from_csv(data_file):
    df = pd.read_csv(data_file, header=0)

    data = df.filter(items=[Feature.MONTH, Feature.DAY, Feature.HOUR,
                            Feature.HOUR, Feature.SP, Feature.SN, Feature.SH])
    labels = df.filter(items=[Output.HEATING, Output.COOLING ])
    return data, labels


def load_data_from_db(table='dbo.building_data'):

    query = "SELECT * FROM {}".format(table)
    df = pd.read_sql(query, cnxn)

    dt_name = df.columns[2]
    b_vol_name, RVal_name, setpoint_name, radnorm_name, radhor_name, outtemp_name, humidity_name, heating_name, cooling_name = \
        df.columns[1], df.columns[3], df.columns[4], df.columns[5], df.columns[6], df.columns[7], df.columns[9], df.columns[10], df.columns[11]

    df['month'] = df.apply(lambda row: row[dt_name].month, axis=1)
    df['day'] = df.apply(lambda row: row[dt_name].day, axis=1)
    df['hour'] = df.apply(lambda row: row[dt_name].hour, axis=1)
    attributes_df = df.filter(items=[b_vol_name, 'month', 'day', 'hour', RVal_name, setpoint_name, radnorm_name, radhor_name, outtemp_name, humidity_name])
    labels_df = df.filter(items=[heating_name, cooling_name])

    return attributes_df.values, labels_df.values

def getRVal():
    return 100

def add_to_database(data_file):
    query = '''
            INSERT INTO dbo.building_data
           ([buildingName]
           ,[buildingVolume]
           ,[inDatetime]
           ,[RValue]
           ,[setPoint]
           ,[irradiationNorm]
           ,[irradiationHor]
           ,[outsideTemp]
           ,[location]
           ,[humidity]
           ,[heating]
           ,[cooling])
            VALUES
           (?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?
           ,?)'''
    data = pd.read_csv(data_file, header=0)
    complete_data(data)

    vals = [(data[data.columns[0]][i],
            float(data[data.columns[1]][i]),
            datetime.datetime(1970, data[data.columns[2]][i], data[data.columns[3]][i], data[data.columns[4]][i], 0, 0),
            getRVal(),
            data[data.columns[5]][i],
            float(data[data.columns[6]][i]),
            float(data[data.columns[7]][i]),
            data[data.columns[8]][i],
            data[data.columns[9]][i],
            data[data.columns[10]][i],
            data[data.columns[11]][i],
            data[data.columns[12]][i]) for i in range(len(data))]

    cursor.executemany(query, vals)
    cnxn.commit()

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


def generate_table(data, form):
    #create header
    excluded = ['estimate', 'input_file', 'csrf_token']
    headers = [f.name for f in form if f.id not in excluded]
    headers.extend(['heating', 'cooling'])

    results = [f.data for f in form if f.id not in excluded]
    results.extend(data[0])

    return [headers, results]

