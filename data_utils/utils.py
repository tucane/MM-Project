import pandas as pd
import numpy as np
import pyodbc
import datetime
from data_utils.data_utils import complete_data, getRValue

########################
# Database credential
########################
host_name = ''
database_name = ''
user_name = ''
pwd = ''
#########################

driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
if not driver_names:
    raise Exception("No pyodbc driver to connect to database")
cnxn = pyodbc.connect(driver=driver_names[0], host=host_name, database=database_name,
                      user=user_name, password=pwd)
cursor = cnxn.cursor()

'''
Old stuff following old attributes. Probably safe to delete
'''
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

'''
Old stuff following old attributes. Probably safe to delete
'''
class Output:
    '''
    COOLING = 'Total Space Cooling - Kwh'
    HEATING = 'Heating - kWh'
    LIGHTING = 'Lighting End-Use Energy - Kwh'
    '''
    HEATING = 'HeatingEnergy'
    COOLING = 'CoolingEnergy'

'''
Old stuff following old attributes. Probably safe to delete
'''
def load_data_from_csv(data_file):
    df = pd.read_csv(data_file, header=0)

    data = df.filter(items=[Feature.MONTH, Feature.DAY, Feature.HOUR,
                            Feature.HOUR, Feature.SP, Feature.SN, Feature.SH])
    labels = df.filter(items=[Output.HEATING, Output.COOLING ])
    return data, labels

'''
load both the input attributes and ground-truth labels 
'''
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

#Just a hack here, since some of our data has 24:00 as 0:00
def get_hour(hour):
    if hour == 24:
        return 0
    return hour

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

    #it seems that cnxn can't take numpy.int64 type. So converting numbers to float
    vals = [(data[data.columns[0]][i],
            float(data[data.columns[1]][i]),
            datetime.datetime(1970, int(data[data.columns[3]][i]), int(data[data.columns[4]][i]), get_hour(int(data[data.columns[5]][i])), 0, 0),
            getRValue(data[data.columns[2]][i]),
            float(data[data.columns[6]][i]),
            float(data[data.columns[7]][i]),
            float(data[data.columns[8]][i]),
            float(data[data.columns[9]][i]),
            data[data.columns[10]][i],
            float(data[data.columns[11]][i]),
            float(data[data.columns[12]][i]),
            float(data[data.columns[13]][i])) for i in range(len(data))]

    cursor.executemany(query, vals)
    cnxn.commit()




