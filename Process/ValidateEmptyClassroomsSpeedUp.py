from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from Colors.Colors import bcolors
import re

class ValidateEmptyClassroomsSpeedUp:
    def __init__(self, driver, school_id, env):
        self.driver = driver
        self.school_id = school_id
        self.env = env

    def run(self):
        res = {}
        try:
            url = f'https://{self.env}sis.amco.me/school_admin/schools/{self.school_id}/classrooms/speedup?query%5Bper_page%5D=5000'
            self.driver.get(url)
            try:
                pg_source = self.driver.page_source
                if ('You have not yet created Classrooms' in pg_source or 'Aun no has creado Aulas' in pg_source):
                    res = {'school_id': self.school_id, 'status': 'Done - 0 Classrooms'}
                    print(f"{bcolors.OKGREEN}School: {self.school_id} Status: Done - 0 Classrooms{bcolors.ENDC}")
                elif(url != self.driver.current_url and 'ticket' not in self.driver.current_url):
                    print(f"{bcolors.OKGREEN}School: {self.school_id} Status: Done - 0 Classrooms{bcolors.ENDC}")
                    res = {'school_id': self.school_id, 'status': 'Done - 0 Classrooms'}
                else:
                    totalStudentsEnrolled = 0
                    total_aulas = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div[4]/div/div/div/div/div/div[1]/div[1]/div[2]")
                    targetAulas = int(re.search(r'\d+', total_aulas.text).group())
                    for j in range(3, targetAulas + 3):        
                        aula_actual = self.driver.find_element(by=By.XPATH, value=f"/html/body/div[1]/div/div/div[4]/div/div/div/div/div/div[{j}]/div/div/div[2]/div[1]")
                        actStudents = int(re.search(r'\d+', aula_actual.text).group())
                        totalStudentsEnrolled = totalStudentsEnrolled + actStudents
                    if totalStudentsEnrolled == 0:
                        print(f"{bcolors.OKGREEN}School: {self.school_id} Status: Done{bcolors.ENDC}")
                        res = {'school_id': self.school_id, 'status': 'Done'}
                    else:
                        print(f"{bcolors.FAIL}School: {self.school_id} Status: Error on Data{bcolors.ENDC}")
                        res = {'school_id': self.school_id, 'status': 'Classrooms with Students'}
            except:
                print(f"{bcolors.FAIL}School: {self.school_id} Status: Validate API Version{bcolors.ENDC}")
                res = {'school_id': self.school_id, 'status': 'Validate URL'}

        except Exception as e:
            print(f"{bcolors.FAIL}Validate URL{bcolors.ENDC}")
        return res