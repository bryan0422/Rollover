import time
import unittest
import sys

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
sys.path.append("..")
from funciones.Funciones import Funciones_Globales

t = 1.5

class base_test(unittest.TestCase):

    def setUp(self):
        self.driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        t = 3

    def test1(self):
        driver = self.driver
        f = Funciones_Globales(driver)
        f.Navegar("https://demoqa.com/buttons", t)
        #elemento = driver.find_element(by= By.XPATH, value="//button[contains(.,'Double Click Me')]")
        f.Click_Double("xpath", "//button[contains(.,'Double Click Me')]")


        time.sleep(2)


if __name__ == '__main__':
    unittest.main()
