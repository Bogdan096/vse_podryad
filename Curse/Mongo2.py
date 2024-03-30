import itertools

from prettytable import PrettyTable
import requests
from bs4 import BeautifulSoup
import pandas as pd
import statistics
import scipy
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from  ordered_set import OrderedSet
ids = []
naming = []
depos_regions = []
depos_val = []
len_check = []
all_period = []
all_val = []
all_val_df = []
unique_rg = []
balance_data = {}
trd_data = {}
all_data = {}
t_dict = {}
t_list = []
general_list = []
urg_val = []
urg_val_df = []
OD_val = []
OD_val_df = []
place = []
tbl_list = ["DT_NSO_0300_027V1", "DT_NSO_1700_002V1"]
url = "https://opendata.1212.mn/api/Data?type=xml"
url2 = "https://opendata.1212.mn/api/Data?type=json"
names = ["Все депозиты", "Депозит до востребования", "Срочные вклады"]
datas = {
    "tbl_id": "DT_NSO_0700_021V1" ,
    "Period": ["2010", "2011"]
}



resp = requests.post(url2, json=datas)
resp2 = requests.post(url, json=datas)
soup = BeautifulSoup(resp.text, "lxml").text
soup2 = BeautifulSoup(resp2.text, "lxml")


regions = soup2.findAll("scr_eng1")
for elem in regions:
    depos_regions.append(elem.text)
print(len(depos_regions))
# print(OrderedSet(depos_regions))

# periods = soup2.findAll("period")
# for elem in periods:
#     period.append(elem.text)
# print(len(period)/11)
var = soup.split("},{")

t_list = ["2011"]
for el in var:
    period = el.split(":")[2].split(",")[0].replace('"', '')
    all_period.append(period)
    if "2010" in el:
        period = el.split(":")[2].split(",")[0].replace('"', '')
        len_check.append(period)
    for elem in t_list:
        if "Нийт хадгаламж" in el and elem in el:
            srez = el.split(":")[-1].replace('"', '')
            ids.extend((elem, srez))

general_list = ids
# print(len(general_list))
# print(general_list[len(general_list)-1])
# print(general_list)
# for elem in t_list:
#     for i in range(0, len(general_list)):
#         try:
#             if elem in general_list[i]:
#                 print("BIGCOCK")
#                 general_list.pop(i)
#         except (IndexError):
#             print('')
# print(general_list)
# slovar = {
#     "Аймаки": depos_regions,
#     "2011": general_list
# }
# df = pd.DataFrame(slovar)
# print(df)
# ordnung= OrderedSet(general_list)
# # n = int((len(ordnung)) / 2)
# n = 356
# res = [ordnung[i:i + n] for i in range(0, len(ordnung), n)]
# for el in res:
#     print(len(el))
#     print(el)
# print(OrderedSet(general_list))


    # if "Нийт хадгаламж" in el:
    #     srez = el.split(":")[-1].replace('"', '')
    #     all_val.append(srez)
        # period = (el.split(":")[3].split(",")[1].replace('"',''))
        # all_val.append(srez)
        # periods.append(period)
    # elif "Хугацаагүй хадгаламж" in el:
    #     srez = el.split(":")[-1].replace('"', '')
    #     OD_val.append(srez)
    # elif "Хугацаатай хадгаламж" in el:
    #     srez = el.split(":")[-1].replace('"', '')
    #     urg_val.append(srez)
len_check = len_check[1:]
all_period = all_period[1:]



# print(len(periods))
# print(periods)
# print((all_val))
# print(len(OD_val))
# print(len(urg_val))




