import requests
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import os
from pandas.io.excel import ExcelWriter
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(category=InsecureRequestWarning)
from multiprocessing import Pool
import sys
import time
names = []
types = []
linkages =[]
prices = []
cardprices = []
names_ga= []
types_ga= []
linkages_ga =[]
prices_ga = []
cardprices_ga= []
articles = []
hrefs = []
pages = []
items = []
items_ga = []
articles_ga = []
sys.setrecursionlimit(10000)
def get_page_data_brn(href, page):
    start = time.time()
    link = "https://znakooo.ru" + href + f"?PAGEN_4={page}"
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
    old_pr = soup.find_all(class_="name p-product__title")
    for op in old_pr:
        hrf = op.find("a").get("href")
        last_link = "https://znakooo.ru" + hrf
        linkages.append(last_link)
        try:
            response = requests.get(last_link)
            soup = BeautifulSoup(response.text, 'lxml')

        except(requests.exceptions.ConnectTimeout):
            print("r", end="")
            continue
        name = soup.find(class_="product-title").text
        names.append(name)
        cardprice = soup.find(class_="p-price p-price_strong").text.strip()
        cardprices.append(cardprice)
        type = soup.find(class_="p-price").text.strip()
        price = type.split("руб.")[0]
        prices.append(price)
        if "шт" in type:
            types.append("Цена ЗнакБарнаул за шт")
        elif "Уп" in type:
            types.append("Цена ЗнакБарнаул за Уп")
        elif "пог. м" in type:
            types.append("Цена ЗнакБарнаул за пог. м")
        article = soup.find_all(class_="product-characteristics")
        for art in article:
            a = art.find_all("span")
            artings = a[-1:]
            for val in artings:
                articles.append(val.text)
    end = time.time()
    return names, articles, types, prices, cardprices







# def get_page_data_ga(href, page):
#     start = time.time()
#     link = "https://galtaysk.znakooo.ru"+ href + f"?PAGEN_4={page}"
#     response = requests.get(link)
#     soup = BeautifulSoup(response.text, "lxml")
#     old_pr = soup.find_all(class_="name p-product__title")
#     for op in old_pr:
#         hrf = op.find("a").get("href")
#         last_link = "https://galtaysk.znakooo.ru" + hrf
#         try:
#             response = requests.get(last_link)
#             soup = BeautifulSoup(response.text, 'lxml')
#         except(requests.exceptions.ConnectTimeout):
#             print("r", end="")
#             continue
#         name = soup.find(class_="product-title").text
#         cardprice = soup.find(class_="p-price p-price_strong").text.strip()
#         type = soup.find(class_="p-price").text.strip()
#         price = type.split("руб.")[0]
#         if "шт" in type:
#             types_ga.append("Цена ЗнакМайма за шт")
#         elif "Уп" in type:
#             types_ga.append("Цена ЗнакМайма за Уп")
#         elif "пог. м" in type:
#             types_ga.append("Цена ЗнакМайма за пог. м")
#         article = soup.find_all(class_="product-characteristics")
#         for art in article:
#             a = art.find_all("span")
#             artings = a[-1:]
#             for val in artings:
#                 articles_ga.append(val.text)
#             names_ga.append(name)
#             cardprices_ga.append(cardprice)
#             linkages_ga.append(last_link)
#             prices_ga.append(price)
#     end = time.time()


def gather_data_brn():
    url = 'http://znakooo.ru/catalog/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    btn = soup.find_all(class_="collection")
    for group in btn:

        group_href = group.find("a").get("href").strip()

        x = url[:-9] + group_href
        respon = requests.get(x)
        soup = BeautifulSoup(respon.text, 'lxml')

        mxpgs = soup.find("div", class_="products__list products__list_e1").get("data-showmore").split(",")

        max_page = mxpgs[0]
        for i in range(1, int(max_page) + 1):
            items.append((group_href, i))





def gather_data_ga():
    url = 'http://galtaysk.znakooo.ru/catalog/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    btn = soup.find_all(class_="collection")
    for group in btn:

        group_href = group.find("a").get("href").strip()

        x = url[:-9] + group_href
        respon = requests.get(x)
        soup = BeautifulSoup(respon.text, 'lxml')

        mxpgs = soup.find("div", class_="products__list products__list_e1").get("data-showmore").split(",")

        max_page = mxpgs[0]
        for i in range(1, int(max_page) + 1):
            items_ga.append((group_href, i))


def main():
    new_slovar = {
        "Код": 1,
        "Конкуренты": "Знак Барнаул",
        "Артикул": articles,
        "Наименование": names,
        "Вид цены": types,
        "Цена": prices,
        "Цена по карте": cardprices,
        "Ссылка": linkages
    }
    # new_slovar_ga = {
    #     "Код": 1,
    #     "Конкуренты": "Знак Майма",
    #     "Артикул": articles_ga,
    #     "Наименование": names_ga,
    #     "Вид цены": types_ga,
    #     "Цена": prices_ga,
    #     "Ссылка": linkages_ga
    # }

    df = pd.DataFrame(new_slovar)


    # df2 = pd.DataFrame(new_slovar_ga)
    path = os.path.abspath("../Выгрузка цен Знак1.xlsx")
    if os.path.exists(path):
        flag = open(path, "r")
        flag.close()
        os.remove(path)
        path = os.path.abspath("../Выгрузка цен Знак1.xlsx")
        writer = pd.ExcelWriter("Выгрузка цен Знак1.xlsx", engine="xlsxwriter")
        df.to_excel(writer,
                    sheet_name="Барнаул",
                    index=False)
        # df2.to_excel(writer,
        #             sheet_name="Майма",
        #             index=False)
    else:
        with ExcelWriter(path, mode="w") as writer:
            df.to_excel(writer, sheet_name="Барнаул")
            # df2.to_excel(writer, sheet_name="Майма")
    path = os.path.abspath("../Выгрузка цен Знак1.xlsx")


if __name__ == "__main__":
# 	while True:
# 		if datetime.datetime.now().hour == 7:
# main()
# 			time.sleep(60 * 60 * 24)
# 		time.sleep(60 * 20)
    start = time.time()

    gather_data_brn()
    #gather_data_ga()

    pool = Pool(processes=60)
    pool.starmap(get_page_data_brn,items)
    # pool.starmap(get_page_data_ga,items_ga)
    main()
    end = time.time()
    print(end-start)

