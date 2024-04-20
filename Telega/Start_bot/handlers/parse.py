import os
import pandas as pd



def name_parse():
    path = os.path.abspath("../Сотрудники.xlsx")
    df = pd.read_excel(path)
    return (df["Сотрудники"].tolist())


name_parse()