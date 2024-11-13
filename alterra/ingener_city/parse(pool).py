import aiohttp
import asyncio
from selectolax.parser import HTMLParser
import time
import pandas as pd
import os
async def get_response(session, url, retries=3):
    """Получение ответа от сервера с обработкой ошибок"""
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=50) as response:
                response.raise_for_status()  # Проверка на ошибки HTTP
                return await response.text()
        except (aiohttp.ClientTimeout, aiohttp.ClientError) as e:
            print(f"Network error occurred: {e}. Attempt {attempt + 1} of {retries}. Retrying...")
            await asyncio.sleep(2)  # Ожидание перед повторной попыткой
        except asyncio.TimeoutError:
            print(f"Timeout error occurred for URL: {url}. Attempt {attempt + 1} of {retries}. Retrying...")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"An unexpected error occurred while requesting {url}: {e}")
            break  # Выход из цикла при других ошибках
    return None  # Возвращаем None, если не удалось получить ответ

async def parse_categories(session):
    """Парсинг категорий товаров"""
    response_text = await get_response(session, 'https://barnaul.ingenerseti.ru/catalog/')
    if response_text is not None:
        parser = HTMLParser(response_text)
        cat_links = [f'https://barnaul.ingenerseti.ru{categories.attributes.get("href")}' for categories in
                     parser.css('ul.sf-menu a')]
        return cat_links
    return []
async def parse_goods(session):
    """Парсинг ссылок на товары"""
    cat_links = await parse_categories(session)
    supply_path = []
    for el in cat_links:
        print(f"cat_links: {el}")
        while True:
            response_text = await get_response(session, el)
            if response_text is not None:
                parser = HTMLParser(response_text)
                good_links = [el + item.attributes.get("href") for item in
                              parser.css('div.description div.desc_name a')]
                # Пагинация
                next_page = None
                for ell in parser.css("ul.pagination li a.pager-nav"):
                    if "right" in ell.attributes.get("class"):
                        next_page = f'https://barnaul.ingenerseti.ru{ell.attributes.get("href")}'
                        break
                if next_page:
                    supply_path.append(el)
                    el = next_page
                else:
                    break
            else:
                break
    return supply_path


async def parse_products(session):
    """Парсинг информации о товарах"""
    supply_path = await parse_goods(session)
    product_links = []
    article_list = []
    name_list = []
    price_list = []
    for elem in supply_path:
        print(f"elem = {elem}")
        response_text = await get_response(session, elem)
        if response_text is not None:
            parser = HTMLParser(response_text)
            good_links = [("/").join(elem.split("/")[:-1]) + item.attributes.get("href") + elem.split("/")[-1] for item
                          in parser.css('div.description div.desc_name a')]
            tasks = []
            for goods in good_links:
                tasks.append(parse_product_details(session, goods, product_links, article_list, name_list, price_list))
            await asyncio.gather(*tasks)
    return product_links, article_list, name_list, price_list

async def parse_product_details(session, goods, product_links, article_list, name_list, price_list):
    """Парсинг информации о конкретном товаре"""
    print(goods)
    response_text = await get_response(session, goods)
    if response_text is not None:
        parser = HTMLParser(response_text)
        status = parser.css("div.product__status")
        strange_check = parser.css("div.product__prices div.col-md-12")
        for el, elem in zip(status, strange_check):
            if ("out-of-stock" not in el.attributes.get("class") and "-by-request" not in el.attributes.get(
                    "class") and elem.text(strip=True)):
                product_links.append(goods)

                name = parser.css("div.col-md-12 h1")
                article = parser.css("div.detail_product_code")
                prices = parser.css("span.product__price")

                for price in prices:
                    if "old" not in price.attributes.get("class"):
                        price_list.append(float(price.text().split("руб")[0]))

                for art in article:
                    article_list.append(art.text().split(":")[1])

                for nam in name:
                    name_list.append(nam.text())
async def main():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        product_links, article_list, name_list, price_list = await parse_products(session)
        new_slovar = {
            "Код конкурента": 1,
            "Конкурент": "Инженерные сети",
            "Артикул": article_list,
            "Наименование": name_list,
            "Вид цены": "Цена на сайте",
            "Цена": price_list,
            "Ссылка": product_links
        }
        df = pd.DataFrame(new_slovar)

        file_path = "../Парсер ИнжСеть.xlsx"

        if os.path.exists(file_path):
            os.remove(file_path)

        df.to_excel(file_path, sheet_name="Лист 1", index=False)

        print("Парсинг выполнен")
    end = time.time()
    print("Время",(end-start))

if __name__ == "__main__":
    asyncio.run(main())


