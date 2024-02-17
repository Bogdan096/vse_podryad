import requests
from bs4 import BeautifulSoup
import json
from typing import Dict


def get_requisits(borsch: "BeautifulSoup", diction: Dict[str, dict]) -> None:
    """Получаем основные реквизиты позиций и добавляем их в словарь"""
    link = "https://formulam2.ru" + borsch.find(class_="product-card__title").find("a").get("href")
    name = borsch.find(class_="product-card__title").text.strip()
    article = borsch.find(class_="product-card__index").text.replace("Код:", '').strip()
    price = float(borsch.find(class_="product-card__new-price").find("span").text.replace(' ', '').strip())
    diction[article] = dict(Наименование=name, Цена=price, Ссылка=link)


def get_max_page(url: str) -> int:
    """Получаем максимальное количество страниц в каталоге"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    try:
        max_page = int(soup.find_all(class_="pagination__link")[-1].text.strip())
    except (IndexError, TypeError):
        max_page = 1
    return max_page


slovar = {}
page = get_max_page()
for nump in range(1, page+1):
    response = requests.get(f"{}?PAGEN_1={nump}")
    soup = BeautifulSoup(response.text, "lxml")
    goods = soup.find_all("div", class_="product-card products-grid__item")
    for good in goods:
        get_requisits(good, slovar)
    print(nump)
    print(str(nump) + "/" + str(page), end="\r")

with open("Pars_complet.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(slovar, ensure_ascii=False, indent=4))






