import datetime

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict

slovar = {}
def values(dictionary: dict):
    url = "https://finance.rambler.ru/currencies/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    ten_val = soup.find("a", title="Казахских тенге")
    dol_val = soup.find("a", title="Доллар США")
    eur_val = soup.find("a", title="Евро")
    ju_val = soup.find("a", title="Китайских юаней")
    tenge_val = ten_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
    dollar_val = dol_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
    euro_val = eur_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
    juang_val = ju_val.find("div",
                             class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()

    dictionary["Тенге"] = round(float(tenge_val)/100, 4)
    dictionary["Доллар"] = float(dollar_val)
    dictionary["Евро"] = float(euro_val)
    dictionary["Юань"] = float(juang_val) / 10

values(slovar)

key = slovar.keys()

print(list(key)[1])






