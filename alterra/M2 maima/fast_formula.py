import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import os
from pandas.io.excel import ExcelWriter
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(category=InsecureRequestWarning)
import asyncio
import aiohttp

names = []
types = []
linkages =[]
prices = []
articles = []

async def get_page_data_brn(session, href, page):
    print("huy grarega")
    link = f"{href}?PAGEN_4={page}"
    print(link)
    async with session.get(link) as response:
        print("ohayou")
        request = response.text
        soup = BeautifulSoup(await request(), "lxml")
        goods = soup.find_all("div", class_="product-card products-grid__item")
        # print(goods)
        # for good in goods:
        #     print("hehey")
        #     hrf = good.find(class_="product-card__title").find("a").get("href")
        #     blink = "https://gorniy.formulam2.ru/" + hrf
        #     name = good.find(class_="product-card__title").text.strip()
        #     article = good.find(class_="product-card__index").text.replace("Код:", '').strip()
        #     price = float(good.find(class_="product-card__new-price").find("span").text.replace(' ', '').strip())
        #     type = "Цена ФормулаМ2Горный за" + good.find("div", class_="product-card__new-price").text.split("/")[1]
        #
        #     types.append(type)
        #     linkages.append(blink)
        #     names.append(name)
        #     prices.append(price)
        #     articles.append(article)
        #     print(prices)
        #     print(linkages)
        #     print(types)



 link = "https://znakooo.ru"+ href + f"?PAGEN_4={page}"

async def gather_data_brn():

    url = 'https://gorniy.formulam2.ru/catalog/'
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), 'lxml')
        links = soup.find_all("div", class_="catalog-sections-item__img")
        for lin in links:

            link = "https://gorniy.formulam2.ru/" + lin.find("a")["href"]
            response = await session.get(link)
            soup = BeautifulSoup(await response.text(), "lxml")
            try:
                max_page = int(soup.find_all(class_="pagination__link")[-1].text.strip())
            except (IndexError, TypeError):
                max_page = 1

            tasks =[]
        for i in range(1, int(max_page)):
            task = asyncio.create_task(get_page_data_brn(session, link, i))
            tasks.append(task)
        await asyncio.gather(*tasks)



def main():
    asyncio.run(gather_data_brn())
    # print("gjitk yf[eq")
    # new_slovar = {
    #     "Код": 1,
    #     "Конкуренты": "ФормулаМ2Горный",
    #     "Артикул": articles,
    #     "Наименование": names,
    #     "Вид цены": types,
    #     "Цена": prices,
    #     "Ссылка": linkages
    # }
    #
    # df = pd.DataFrame(new_slovar)
    # path = os.path.abspath("../Выгрузка цен Формула.xlsx")
    # if os.path.exists(path):
    #     flag = open(path, "r")
    #     flag.close()
    #     os.remove(path)
    #     path = os.path.abspath("../Выгрузка цен Формула.xlsx")
    #     df.to_excel("C:\\Users\\Admin\\PycharmProjects\\edu2023\\alterra\\Выгрузка цен Формула.xlsx",
    #                 sheet_name="Лист 1",
    #                 index=False)
    # else:
    #     with ExcelWriter(path, mode="w") as writer:
    #         df.to_excel(writer, sheet_name="Лист 1")
    # path = os.path.abspath("../Выгрузка цен Формула.xlsx")



main()
