import requests
from bs4 import BeautifulSoup
import json
from typing import Dict
import pandas
import os

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                            "Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"}
def get_links(way: str) -> Dict[str, str]:
    df = pandas.read_excel(way, index_col="Название магазина")
    return df.to_dict()


def get_rating(url: str, adres: str, listing: list) -> list:
    response = requests.get(url, headers=header).text
    soup = BeautifulSoup(response, "lxml")
    main = soup.find(class_ = "_1tfwnxl")
    contains = main.find(class_="_y10azs")
    contains2 = main.find(class_="_jspzdm")
    diction = {}
    diction["Количество отзывов"] = contains2.text
    diction["Рейтинг"] = contains.text
    diction["Название магазина"] = adres
    listing.append(diction)



spisok = []
path = os.path.abspath("Список магазинов.xlsx")
links: dict = get_links(path).get("Ссылка")
for key,value in links.items():
    get_rating(value, key, spisok)

dataf = pandas.DataFrame(spisok)
otkritie = pandas.read_excel(path, sheet_name = "Лист1")
df = otkritie.merge(dataf, left_on="Название магазина", right_on="Название магазина")
df.to_excel(path, sheet_name= "Лист1", index=False)
print(df)



