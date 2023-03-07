from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from Colors.Colors import bcolors
from datetime import datetime


class ValidateContract:
    def __init__(self, driver, school_id, env, aluzo_version):
        self.driver = driver
        self.school_id = school_id
        self.env = env
        self.aluzo_version = aluzo_version

    def run(self):
        res = {
            'school_id': self.school_id,
            'valid_aluzo_version': False,
            'status': ''
        }
        try:
            url = f'https://{self.env}sis.amco.me/school_admin/schools/{self.school_id}/settings'
            self.driver.get(url)
            try:
                api_version = self.driver.find_element(by=By.XPATH, value="//*[@id='select2-school_api_version-container']")
                school_year = self.driver.find_element(by=By.XPATH, value="//*[@id='school_year']")
                starts_on = self.driver.find_element(by=By.XPATH, value="//*[@id='starts_on']")
                ends_on = self.driver.find_element(by=By.XPATH, value="//*[@id='ends_on']")
                aluzo_version = self.driver.find_element(by=By.XPATH, value="//body[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[7]/div[1]/div[1]/div[2]/div[1]/div[2]/strong[2]")
                if (api_version.text == '3 - Approve classroom'
                    and school_year.get_attribute('value') == '2022'
                    and starts_on.get_attribute('value') in ('2022-07-31' , '2023-07-30')
                    and ends_on.get_attribute('value') == '2023-07-30'):
                    print(f"{bcolors.OKGREEN}School: {self.school_id} Status: Done{bcolors.ENDC}")
                    valid_aluzo_version = int(aluzo_version.text) == self.aluzo_version
                    if valid_aluzo_version:
                        print(f"{bcolors.OKGREEN}Version Aluzo: {int(aluzo_version.text)}")
                    else:
                        print(f"{bcolors.FAIL}Tu aluzo version es: {int(aluzo_version.text)}")
                    res['status'] = 'Done'
                    res['valid_aluzo_version'] = valid_aluzo_version
                else:
                    print(f"{bcolors.FAIL}School: {self.school_id} Status: Error on Data{bcolors.ENDC}")
                    res = {'school_id': self.school_id, 'status': 'Error on Data'}
            except Exception as e:
                print(f"{bcolors.FAIL}School: {self.school_id} Status: Api Version{bcolors.ENDC}")
                res = {'school_id': self.school_id, 'status': 'Api Version'}
        except:
            print(f"{bcolors.FAIL}Validate URL{bcolors.ENDC}")
            res = {'school_id': self.school_id, 'aluzo_version': self.aluzo_version, 'status': 'Validate URL'}
        return res
