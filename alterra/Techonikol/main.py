import requests
from bs4 import BeautifulSoup

from alterra.parser import Parser
from typing import Dict
import pandas as pd
import os
from pandas.io.excel import ExcelWriter
from openpyxl import *






class ParserTechnonikol():
    def __init__(self):
        self.url = "https://barnaul.tstn.ru/"
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/104.0.0.0 Safari/537.36"}
        self.catalog_url = {}
        self.max_page = []
        self.group_name = []
        self.products_by_page={}
    def get_catalog(self):
        response = requests.get(self.url, headers=self.header)
        soup = BeautifulSoup(response.text, "lxml")
        groups = soup.find_all("div", class_="catalog-menu__item")
        for group in groups:
            group_name = group.find(class_="catalog-menu__link-text").text.strip()
            self.group_name.append(group_name)
            group_href = group.find("a").get("href")
            self.catalog_url[group_name] = self.url[:-1] + group_href


    def get_max_page(self):
        for pg_href in self.catalog_url.values():
            response = requests.get(pg_href,headers=self.header)
            soup = BeautifulSoup(response.text, "lxml")
            pages = soup.find_all(class_="pagination__nav-item")
            for page in pages:
                self.max_page.append(page)
            max_page = self.max_page[-1]
            for gr_name in self.group_name:
                self.products_by_page[gr_name] = pg_href + f"?PAGEN_1={max_page}"


    def get_product_info(self):
        for url in self.products_by_page.values():
            response = requests.get(url, headers=self.header)
            soup = BeautifulSoup(response.text, "lxml")
            names = soup.find_all(class_ ="b-product__title")
            articles = soup.find_all(class_="b-product__article")
            types = soup.find_all(class_="price-block__type")
            prices = soup.find_all(class_="price-block__price b-price")
            links = soup.find_all(class_="b-product__wrap")
            for link in links:
                product_link = link.find("a").get("href")
            for price in prices:
                product_price = price.text.split("<sup>")[0]
            for type in types:
                product_type = type.text
            for article in articles:
                pass
            for name in names:
                product_name = name.text



