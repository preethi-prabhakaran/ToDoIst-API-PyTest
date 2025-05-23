from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from config.locators import username_xpath, password_xpath, login_button_xpath, notifications_path


class LoginPage:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password


    def launch_todoist(self):
        driver = webdriver.Chrome()
        driver.get(self.url)

        driver.maximize_window()
        return driver

    def login_to_todoist(self, driver:WebDriver):
        username_input = WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, username_xpath)))
        username_input.send_keys(self.username)

        password_input = WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, password_xpath)))
        password_input.send_keys(self.password)

        login_button = driver.find_element(By.XPATH, login_button_xpath)
        login_button.click()

        WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, notifications_path)))




