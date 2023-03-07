from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from Colors.Colors import bcolors

class LoginAmco:
    def __init__(self, driver, username, password, env):
        self.driver = driver
        self.username = username
        self.password = password
        self.env = env

    def amcoid(self):
        try:
            url = f'https://{self.env}id.amco.me'
            self.driver.get(url)
            element = self.driver.find_element(by=By.XPATH, value="//*[@id='user_session_username']").send_keys(self.username)
            element = self.driver.find_element(by=By.XPATH, value="//*[@id='user_session_password']").send_keys(self.password)
            element = self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/form/div/div/div/div[1]/div[5]/input").click()
            print(f"{bcolors.OKGREEN}Successful access to AmcoId{bcolors.ENDC}")
            url = f'https://{self.env}sis.amco.me'
            self.driver.get(url)
        except:
            print(f"{bcolors.FAIL}Failed access to amcoid{bcolors.ENDC}")