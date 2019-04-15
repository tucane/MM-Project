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

Project Setup
--------
* download the code
* load the code in a Python IDE (I used Pycharm)
* create a virtual environment with all the dependencies in ./requirements.txt

Section Breakdown:
--------
### ML Model Training
The backend ML model is trained using RandomForestRegressor in scikit-learn. 
##### The model has following input attributes:
* building volume
* input month
* input day
* input hour
* R value
* setpoint temperature
* solar irradiation normal and horizontal
* outside temperature
* relative humidity

##### The model output are:
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


Most of which are variables used in the ML model, with a few bookkeeping variables such as building name. <br />
Note: the ML prediction is hourly, but the prediction that the building managers see is aggregated daily sum.
The user can manully input the fields in the website, or upload the input as a csv file. Csv file input follows a slightly different format, see MM_Fullstack/example_input/example.csv


The website will consequently make prediction based on the input, and plot the results visually.


The users can also compare how the energy consumption differs by changing some of the input attributes. The user can click the **Switch To Comparative Input** button to use the comparing feature, where the following attributes take both an original and alternative value:
* building volume
* building cladding type
* setpoint temperature
* relative humidity
Where the prediction will plot graphs that compare the original and alternative energy comsumption instead.

##### Usage
Simply execute deploy_app.py with no arguments to run the flask web app locally.

### Script for the developers to maintain the database and train new models
This is a helper script for the developers who are responsible for this project to 
* maintain the database 
* re-train the models.
We don't currently have much data in our hand, as building data may be sensitive information, and require a lot of effort to obtain them. The developers can always add more data to the data base and re-train the backend model.

##### Database setup
The database will need to be re-setup to continue the project, as I am using the database in my personal Azure account. The database only has 1 table named building_data (since that's all it needs for now), with the following columns:
* buildingName(varchar)
* buildingVolume(real)
* inDatetime(datetime)
* RValue(real)
* setPoint(real)
* irradiationNorm(real)
* irradiationHor(real)
* outsideTemp(real)
* location(varchar)
* humidity(real)
* heating(real)
* cooling(real)

and update **data_utils.utils.py** for the new database connection. I created my database in the Azure portal and modified the configuration in MicroSoft SQL Server Managment Studio.

##### Adding new data to database
Given a csv training data file (see MM_Fullstack/example_input/example-training.csv). The developer can exeucte <br />
`main.py add MM_Fullstack/example_input/example-training.csv` to add the new data to database. <br />

##### Training new model for the website
The developer can re-train the model using all the data in the database by executing <br />
`main.py train MM_Fullstack/weights/<new_model_filename>`

### Hosting the website on Azure
Similar to the database, this part needs to be re-setup since I am currently using my person Azure account to host the website.
Follow this guide https://code.visualstudio.com/docs/python/tutorial-deploy-app-service-on-linux <br />
The Azure startup file has already been created (./startup.txt).

Future Improvement/TODO
--------


FAQ/Problems That I've Encountered
--------
Q: Database connection error? <br />
A: Make sure that your IP addressed is added in whitelisted in the Azure Firewall Settings. Double check that your computer has a ODBC driver for SQL.
<br /> <br />
Q: Pandas error when parsing the csv files? <br />
A: Make sure that the order of the columns follows the example format exactly. Delete any empty rows at the bottom of the csv files. 

