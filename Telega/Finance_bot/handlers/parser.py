import requests
from bs4 import BeautifulSoup
import json
from typing import Dict

slovar = {}
def tenge(dictionary: dict):
    url = "https://finance.rambler.ru/currencies/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    prom_val = soup.find("a", title="Казахских тенге")
    value = prom_val.find("div", class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
    dictionary["Тенге"] = float(value)/100

def world_values(diction: dict):
    url = "https://cbr.ru/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    value = soup.find_all("div", class_="col-md-2 col-xs-9 _right mono-num")
    for course in value[:2]:
        diction["Юань"] = course.text.strip()
    for course in value[2:4]:
        diction["Доллар"] = course.text.strip()
    for course in value[4:6]:
        diction["Евро"] = course.text.strip()


tenge(slovar)
world_values(slovar)
print(slovar)






