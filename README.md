APS490 Capstone Project With Mott MacDonald Canada
========

Author: Bill Gan (billgan96@gmail.com)
--------
### Capstone Members: 
* Bill(Jianing) Gan
* Da Da 
* Elton(Siqi) Zhang
* Sijia Ding


Project Overview:
--------
The goal for this project is to provide a machine learning solution for building managers to monitor their building performance and 
potentially increase the building energy efficiency.

Project Detail:
--------
We have implemented the basic machine learning model to predict the expected building energy efficiency, as well as a website for the 
building managers to upload and predict their building energy data. <br />
Due to limited resource, we were not able to make an energy optimization 
solution using deep reinforcement learning. (for example, https://arxiv.org/pdf/1903.05196.pdf)

The project can be broken into three major parts:
1. Website with the ML model in the backend for the building manager to use
2. Script for the developers to maintain the database and train new models
3. Hosting the website on Azure

Section Breakdown:
--------
### ML Model Training
The backend ML model is trained using RandomForestRegressor in scikit-learn. 
#### The model has following input attributes:
* building volume
* input month
* input day
* input hour
* R value
* setpoint temperature
* solar irradiation normal and horizontal
* outside temperature
* relative humidity

#### The model output are:
* heating load
* cooling load

### Website with the ML model in the backend for the building manager to use
This is the main bulk of the project, where it allows the building managers to upload their own building data to make prediction and visualize the energy consumption trend, and an option to download the prediction trend as a csv file.
The building data that the building manager must provide are:
* building name
* building volume
* prediction from date
* prediction to date
* building cladding type
* setpoint temperature
* solar irradiations
* building location
* outside temperature
* relative humidity
<br />
Where the user can manully input the fields in the website, or upload the input as a csv file. Csv file input follows a slightly different format, please see MM_Fullstack/example_input/example.csv
<br />
The website will consequently make prediction based on the input, and plot the results visually.

Project Code Details
========

Project Folder Structure
--------
    .
    ├── data_utils              # utils module
    │   ├── __init__.py
    │   ├── data_utils.py                      # clean the data or generate the graphs and tables for users to see
    │   └── utils.py                           # load data from csv/database and upload data to database 
    ├── ML_Fullstack            # module that contains the flask web app
    |   ├── .ideas              
    |   ├── example_input       # folder that contains examples training/inferencing csv data files
        │   ├── example.csv                    # format of inferencing data for building managers to upload
        │   ├── example-training.csv           # format of training data for developers to upload
        │   ├── training_data_2.csv       
        │   └── training_Data_winter.csv
    |   ├── static              
        |   └── style.css                      # we have not spent a lot of time to make the website aesthetically pleasing.
    |   ├── templates           
        |   ├── comparative_prediction.html    # showing the prediction result with the comparative input fields
        |   ├── compare.html                   # comparative input fields
        |   ├── index.html                     # default page. Regular input fields
        |   ├── macro.html                     # macro the input page template
        |   └── prediction.html                # showing the prediction result with the regular input fields
    |   ├── weights              # folder that contains the ML models
        |   ├── default_weights.joblib         # the default one that the website uses
        |   ├── default_weights2.joblib        # a few other ones made for testing
        |   └── default_weights3.joblib
    |   ├── __init__.py                                  
    |   ├── application.py                     # standard flask app 
    |   ├── forms.py                           # standard flask WTForms
    |   ├── inference.py                       # making actual prediction given the building data and backend model
    |   ├── README.md
    |   ├── requirements.txt                    
    |   └── web.config                         # was messing around trying to deploy this app on azure. Probably not needed
    ├── MM_Machine_Learning                    # playground module to try out different ML algorithms. Not needed for project
    ├── .gitignore
    ├── __init__.py
    ├── compare.py                             # playground file to test model performance with incomplete data
    ├── deploy_app.py                          # deploy app/run app locally
    ├── main.py                                # script for the developers to maintain database and re-train model
    ├── README.md                              # ME!!!
    ├── requirements.txt                       
    ├── startup.txt                            # start-up file to deploy the app on azure
    └── test_model.py                          # another playground file to test model performance  
