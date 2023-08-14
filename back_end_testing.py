from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time,math,random,os,re
from prettytable import PrettyTable

from selenium import webdriver
import unittest

class BankingPage:
    def __init__(self, driver):
        self.driver = driver

    def deposit(self, amount):
        
        deposit_field = self.driver.find_element(By.ID, "deposit")
        deposit_field.send_keys(amount)
        #print(f"This is deposit field {deposit_field}")

     

    def withdraw(self, amount):
      
        withdraw_field = self.driver.find_element(By.ID, "withdraw")
        withdraw_field.send_keys(amount)

    def submit(self):
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

      
    def get_balance(self):
        time.sleep(random.uniform(5, 9))
        balance = self.driver.find_element(By.ID, "ending_balance")
        balance_text = balance.text
        match = re.search(r'\d+\.?\d*', balance_text)
        if match:
            return float(match.group())
        else:
            raise ValueError(f"Could not extract balance from text: {balance_text}")
        


class TestBankingPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(service=Service(executable_path=r'D:/python_Scripts/Web-Scraping-Project-master/geckodriver.exe'))
       
        self.driver.get("http://127.0.0.1:5000/")
        self.page = BankingPage(self.driver)
        self.expected_balance = self.page.get_balance()
     

    def test_transactions(self):
      
      
        self.page.deposit(100)
        self.page.submit() # Click submit after deposit
        time.sleep(3) # Wait to see the action
        self.assertEqual(self.page.get_balance(), 862.0)
        self.check_balance(100, "Deposit")
       

        self.page.deposit(50)
        self.page.submit() # Click submit after deposit
        time.sleep(3) # Wait to see the action
        self.assertEqual(self.page.get_balance(), 912.0)
        self.check_balance(50, "Deposit")
       

        self.page.withdraw(200)
        self.page.submit() # Click submit after deposit
        time.sleep(3) # Wait to see the action
        self.assertEqual(self.page.get_balance(), 712.0)
        self.check_balance(200, "Withdraw")
       

      

    def check_balance(self, amount, action):
        time.sleep(3)  # Wait to see the action
        if action == 'Deposit':
            self.expected_balance += amount
        elif action == 'Withdraw':
            self.expected_balance -= amount
        actual_balance = self.page.get_balance()
        print(f"{action}: {amount} -> Expected: {self.expected_balance}, Actual: {actual_balance}")
        self.assertEqual(self.expected_balance, actual_balance)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()