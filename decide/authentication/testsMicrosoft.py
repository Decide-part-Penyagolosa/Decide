# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestPp():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
#   def test_pp(self):
#     # Test name: pp
#     # Step # | name | target | value
#     # 1 | open | http://localhost:8000/booth/voting | 
#     self.driver = webdriver.Chrome()
#     self.driver.get("http://localhost:8000/booth/voting")
#     # 2 | setWindowSize | 909x1016 | 
#     self.driver.set_window_size(909, 1016)
#     # 3 | click | css=tr:nth-child(3) a | 
#     self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
#     # 4 | click | xpath=(//div[@id='customBtn']/a/span)[2] | 
#     self.driver.find_element(By.XPATH, "(//div[@id=\'customBtn\']/a/span)[2]").click()
#     # 5 | pause | 5000 | 
#     time.sleep(5)
#     # 6 | type | id=i0116 | innosoft2021.16@gmail.com
#     self.driver.find_element(By.ID, "i0116").send_keys("innosoft2021.16@gmail.com")
#     # 7 | pause | 5000 | 
#     time.sleep(5)
#     # 8 | click | id=idSIButton9 | 
#     self.driver.find_element(By.ID, "idSIButton9").click()
#     # 9 | pause | 5000 | 
#     time.sleep(5)
#     # 10 | type | id=i0118 | Jornada1
#     self.driver.find_element(By.ID, "i0118").send_keys("Jornada1")
#     # 11 | pause | 5000 | 
#     time.sleep(5)
#     # 12 | click | id=idSIButton9 | 
#     self.driver.find_element(By.ID, "idSIButton9").click()
#     # 13 | click | id=idSIButton9 | 
#     self.driver.find_element(By.ID, "idSIButton9").click()
#     # 14 | assertText | css=th:nth-child(1) | Name
#     assert self.driver.find_element(By.CSS_SELECTOR, "th:nth-child(1)").text == "Name"
  

#   def test_pp1(self):
#     # Test name: pp (2)
#     # Step # | name | target | value
#     # 1 | open | http://localhost:8000/booth/voting | 
#     self.driver = webdriver.Chrome()
#     self.driver.get("http://localhost:8000/booth/voting")
#     # 2 | setWindowSize | 909x1016 | 
#     self.driver.set_window_size(909, 1016)
#     # 3 | click | css=tr:nth-child(3) a | 
#     self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) a").click()
#     # 4 | click | xpath=(//div[@id='customBtn']/a/span)[2] | 
#     self.driver.find_element(By.XPATH, "(//div[@id=\'customBtn\']/a/span)[2]").click()
#     # 5 | pause | 5000 | 
#     time.sleep(5)
#     # 6 | type | id=i0116 | innosoft2021.16@gmail.com
#     self.driver.find_element(By.ID, "i0116").send_keys("innosoft2021.166@gmail.com")
#     # 7 | pause | 5000 | 
#     time.sleep(5)
#     # 8 | click | id=idSIButton9 | 
#     self.driver.find_element(By.ID, "idSIButton9").click()
#     # 9 | assertText | id=usernameError | No hemos podido encontrar ninguna cuenta con ese nombre de usuario. Escriba otra dirección u obtenga una nueva cuenta de Microsoft.
#     assert self.driver.find_element(By.ID, "usernameError").text == "No hemos podido encontrar ninguna cuenta con ese nombre de usuario. Escriba otra dirección u obtenga una nueva cuenta de Microsoft."  

