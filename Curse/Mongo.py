from prettytable import PrettyTable
import requests
from bs4 import BeautifulSoup
import pandas as pd
import statistics
import scipy
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

ids = []
naming = []
trd_period = []
trd_volume = []
bal_period = []
bal_value = []
loyal_period = []
loyal_value = []
loyal_data = {}
dt ={}
balance_data = {}
trd_data = {}
all_data = {}
tbl_list = []
r = open("all_info.xml", "r", encoding="utf-8")
xml_open = r.read()
soup = BeautifulSoup(xml_open,"lxml")
name = soup.findAll("tbl_eng_nm")
tbl_id = soup.findAll("tbl_id")
for names in name:
    naming.append(names.text)
for id in tbl_id:
    ids.append(id.text)
for i in range(len(naming)):
    dt[naming[i]]=ids[i]

tbl_list = ["DT_NSO_1400_003V1", "DT_NSO_0800_008V1"]
url = "https://opendata.1212.mn/api/Data?type=xml"
url2 = "https://opendata.1212.mn/api/Data?type=json"

datas = {
    "tbl_id": "DT_NSO_1400_003V1",
    # "Period": ["201506", "201505"]
}
datas1 = {
    "tbl_id": "DT_NSO_0800_008V1",
}
datas2 = {
    "tbl_id": "DT_NSO_0700_010V1",
    # "Period": ["201506", "201505"]
}
resp = requests.post(url, json=datas)
soup = BeautifulSoup(resp.text, "lxml")


# print(soup)
resp1 = requests.post(url, json=datas1)
soup1 = BeautifulSoup(resp1.text, "lxml")

resp2 = requests.post(url2, json=datas2)
soup2 = BeautifulSoup(resp2.text, "lxml").text

var2 = soup2.split("},{")
#

periods = soup.findAll("period")
for elem in periods:
    trd_period.append(int(elem.text))
values = soup.findAll("dtval_co")
for elem in values:
    trd_volume.append(float(elem.text))
for i in range(0, len(trd_period), 4):
    trd_data[trd_period[i]] = trd_volume[i]
all_data["Внешнеторговый оборот"] = trd_data


periods = soup1.findAll("period")
for elem in periods:
    bal_period.append(int(elem.text))
values = soup1.findAll("dtval_co")
for elem in values:
    bal_value.append(float(elem.text))
for i in range(len(bal_period)):
    balance_data[bal_period[i]] = bal_value[i]
all_data["Баланс бюджета общего управления"] = balance_data

for el in var2:
    if "Total liabilities" in el:
        srez = el.split(":")[-1].replace('"','')
        if srez == "success}":
            continue
        loyal_value.append(float(srez))
        loyal_period.append(int(el.split(":")[2].split(",")[0].replace('"','')))

for i in range(len(loyal_period)-1):
    loyal_data[loyal_period[i]] = loyal_value[i]
# print(loyal_data)
all_data["Общие обязательства"] = loyal_data
df = pd.DataFrame(all_data)
print(df)

#
# min_trd_vol = min(trd_volume)
# min_bal_val = min(bal_value)
# min_loyal_val = min(loyal_value)
#
# max_trd_vol = max(trd_volume)
# max_bal_val = max(bal_value)
# max_loyal_val = max(loyal_value)
#
# trd_mean=statistics.mean(trd_volume)
# bal_mean=statistics.mean(bal_value)
# loyal_mean = statistics.mean(loyal_value)
#
# trd_mdn = statistics.median(trd_volume)
# bal_mdn = statistics.median(bal_value)
# loyal_mdn = statistics.median(loyal_value)
# arr = np.array(trd_volume)
# sk = scipy.stats.skew(arr, axis=0, bias=True)
# arr1 = np.array(bal_value)
# sk1 = scipy.stats.skew(arr1, axis=0, bias=True)
# arr2 = np.array(loyal_value)
# sk2 = scipy.stats.skew(arr2, axis=0, bias=True)
#
# exc = scipy.stats.kurtosis(arr, axis=0, bias=True)
# exc1 = scipy.stats.kurtosis(arr1, axis=0, bias=True)
# exc2 = scipy.stats.kurtosis(arr2, axis=0, bias=True)
#
# scope = max_trd_vol-max_bal_val
# scope1 = max_bal_val-min_bal_val
# scope2 = max_loyal_val-min_loyal_val
#
x_bal = np.array(bal_period)
y_bal = np.array(bal_value)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=100))
plt.plot(x_bal,y_bal)
for i, txt in enumerate(y_bal):
    plt.annotate(txt, (x_bal[i], y_bal[i]))
plt.title("Баланс бюджета общего управления")
plt.xlabel("Даты измерений")
plt.ylabel("Значения величины", rotation=90)
plt.show()

# x_trd = np.array(trd_period)
# y_trd = np.array(trd_volume)
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
# plt.gca().xaxis.set_major_locator(mdates.YearLocator())
# plt.plot(x_trd, y_trd)
# plt.show()
#
# x_loyal = np.array(loyal_period)
# y_loyal = np.array(loyal_value)
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
# plt.gca().xaxis.set_major_locator(mdates.YearLocator())
# plt.plot(x_loyal, y_loyal)
# plt.show()

# my_table = PrettyTable()
# my_table.add_column("Величины",["Максимум", "Минимум", "Среднее", "Медиана", "Эксцесс", "Асимметрия", "Размах"])
# my_table.add_column("Внешнеторговый оборот", [max_trd_vol, min_trd_vol, trd_mean, trd_mdn, exc, sk, scope])
# my_table.add_column("Баланс бюджета общего управления", [max_bal_val, min_bal_val, bal_mean, bal_mdn, exc1, sk1, scope1])
# my_table.add_column("Общие обязательства", [max_loyal_val, min_loyal_val, loyal_mean, loyal_mdn, exc2, sk2, scope2])
# print(my_table)


df.to_csv('mongo_stat.csv', header=False)



    

