import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

import requests


url = 'https://barnaul.tstn.ru/'
resp = requests.get(url)
print(resp)
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,"lxml")
print(soup.prettify())

