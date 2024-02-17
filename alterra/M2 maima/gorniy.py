import requests
from bs4 import BeautifulSoup
import json
from typing import Dict
import pandas as pd
import os
from pandas.io.excel import ExcelWriter
from openpyxl import *



def get_requisits(borsch: "BeautifulSoup", diction: Dict[str, dict]) -> None:
    """Получаем основные реквизиты позиций и добавляем их в словарь"""
    blink = "https://gorniy.formulam2.ru/" + borsch.find(class_="product-card__title").find("a").get("href")
    name = borsch.find(class_="product-card__title").text.strip()
    article = borsch.find(class_="product-card__index").text.replace("Код:", '').strip()
    price = float(borsch.find(class_="product-card__new-price").find("span").text.replace(' ', '').strip())
    quantity = borsch.find("div", class_="product-card__new-price").text.split("/")[1]
    diction[article] = dict(Наименование=name, Цена=price, Ссылка=blink,
                            Единица_измерения="Цена ФормулаМ2Горный за" + quantity, Конкуренты="ФормулаМ2Горный")

def get_max_page(url: str) -> int:
    """Получаем максимальное количество страниц в каталоге"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    try:
        max_page = int(soup.find_all(class_="pagination__link")[-1].text.strip())
    except (IndexError, TypeError):
        max_page = 1
        print(max_page)
    return max_page

slovar = {}
response = requests.get("https://gorniy.formulam2.ru/catalog/")
soup = BeautifulSoup(response.text, "lxml")
links = soup.find_all("div", class_="catalog-sections-item__img")
for lin in links[1:3]:
    link = "https://gorniy.formulam2.ru/"+lin.find("a")["href"]

    page = get_max_page(link)
    for nump in range(0, 3):
        response = requests.get(f"{link}?PAGEN_1={nump}")
        soup = BeautifulSoup(response.text, "lxml")
        goods = soup.find_all("div", class_="product-card products-grid__item")
        for good in goods:
            get_requisits(good, slovar)

names = []
articles = []
prices = []
links = []
quantities = []
opponents = []
headers = []
for key, value in slovar.items():
    articles.append(key)
    names.append((slovar[key]["Наименование"]))
    links.append((slovar[key]["Ссылка"]))
    prices.append((slovar[key]["Цена"]))
    quantities.append((slovar[key]["Единица_измерения"]))
    opponents.append((slovar[key]["Конкуренты"]))
new_slovar = {
    "Код": 1,
    "Конкуренты": opponents,
    "Артикул": articles,
    "Наименование": names,
    "Вид цены": quantities,
    "Цена": prices,
    "Ссылка": links
}
df = pd.DataFrame(new_slovar)
path = os.path.abspath("Выгрузка цен (4).xlsx")
if os.path.exists(path):
    flag = open(path, "r")
    flag.close()
    os.remove(path)
    path = os.path.abspath("Выгрузка цен (4).xlsx")
    df.to_excel("C:\\Users\\Admin\\PycharmProjects\\edu2023\\alterra\\Выгрузка цен (4).xlsx", sheet_name="Лист 1", index=False)
else:
    with ExcelWriter(path, mode="w") as writer:
        df.to_excel(writer, sheet_name="Лист 1")



