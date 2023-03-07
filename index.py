from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
from google.cloud import bigquery
import numpy as np
import pandas_gbq
import yaml
from Process.ValidateContract import ValidateContract
from Process.ValidateEmptyClassrooms import ValidateEmptyClassrooms
from Process.ValidateEmptyClassroomsSpeedUp import ValidateEmptyClassroomsSpeedUp
from Login.Login import LoginAmco
import csv
from datetime import datetime


#Define environment
ENVIRONMENT = 'SIS_' + 'LIVE'
#config[ENVIRONMENT]['EMAIL']
#Open config yml
with open("config.yml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

schools = pd.read_csv(config[ENVIRONMENT]['FILE'])

def validateContract():
    statusList = []
    options = Options()
    options.add_experimental_option("detach", True)
    #options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    LoginAmco(driver, config[ENVIRONMENT]['EMAIL'], config[ENVIRONMENT]['PASSWORD'], config[ENVIRONMENT]['SUB']).amcoid()
    for index, row in schools.iterrows():
        status = ValidateContract(driver, row['school_id'], config[ENVIRONMENT]['SUB'], row['aluzo_version']).run()
        statusList.append(status)
    driver.quit()
    actDate = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = f'ValidateContract-{actDate}.csv'
    print(f'Done. File Generated in: {filename}')
    df = pd.DataFrame(statusList)
    df.to_csv(filename, index=False)

def validateEmptyClassrooms():
    statusList = []
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    LoginAmco(driver, config[ENVIRONMENT]['EMAIL'], config[ENVIRONMENT]['PASSWORD'], config[ENVIRONMENT]['SUB']).amcoid()
    for index, row in schools.iterrows():
        status = ValidateEmptyClassrooms(driver, row['school_id'], config[ENVIRONMENT]['SUB']).run()
        statusList.append(status)
    driver.quit()
    actDate = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = f'ValidateClassrooms-{actDate}.csv'
    print(f'Done. File Generated in: {filename}')
    df = pd.DataFrame(statusList)
    df.to_csv(filename, index=False)

def validateEmptyClassroomsSpeed():
    statusList = []
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    LoginAmco(driver, config[ENVIRONMENT]['EMAIL'], config[ENVIRONMENT]['PASSWORD'], config[ENVIRONMENT]['SUB']).amcoid()
    for index, row in schools.iterrows():
        status = ValidateEmptyClassroomsSpeedUp(driver, row['school_id'], config[ENVIRONMENT]['SUB']).run()
        statusList.append(status)
    driver.quit()
    actDate = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = f'ValidateClassroomsSpeedUp-{actDate}.csv'
    print(f'Done. File Generated in: {filename}')
    df = pd.DataFrame(statusList)
    df.to_csv(filename, index=False)



finishFlag = False
while finishFlag == False:
    print('Select a option:')
    print("""
    1.- Validate Contract
    2.- Validate Empty Classrooms
    3.- Validate Empty Speed Up Classrooms
    0.- Exit
    """)
    opt = int(input())
    if opt == 1:
        validateContract()
    if opt == 2:
        validateEmptyClassrooms()
    if opt == 3:
        validateEmptyClassroomsSpeed()
    if opt == 0:
        print('Hasta la vista baby !')
        finishFlag = True