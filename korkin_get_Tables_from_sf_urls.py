# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 01:21:39 2025

@author: User
"""

import requests
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd



values = []
with open("superfamily_ids_from_repeats_db.txt", "r") as scope_207:
    sc_2 = scope_207.readlines()
    for line in sc_2:
        values.append(line[2:])

for value in values[70:]:
    url = f"https://supfam.org/genome/hs/sf/{value}"
    # get = requests.get(url)
    # parsed_html = BeautifulSoup(get)
    # print(parsed_html)
    #timeout_seconds = 180
    #fp = urllib.request.urlopen(f"https://supfam.org/genome/hs/sf/{value}")
    # try:
    response = requests.get(url)
    # except requests.exceptions.Timeout:
    #     print(f"Задержка превышает {timeout_seconds} секунд. Запрос не был выполнен.")
    #     pass
    if response.status_code == 500 or response.status_code == 502:
        print("Произошла ошибка при выполнении запроса:", value)
        pass
    else:
        fp = urllib.request.urlopen(f"https://supfam.org/genome/hs/sf/{value}")
        mybytes = fp.read()
    
        mystr = mybytes.decode("utf8")
        fp.close()
        parsed_html = BeautifulSoup(mystr)
        soup = BeautifulSoup(mystr, "html.parser")
    
        data = []
        for row in soup.find_all("tr"):
            cols = row.find_all("td")
            if not cols:
                continue
            species = cols[0].text.strip()
            protein_id = cols[1].a.text.strip() if cols[1].a else cols[1].text.strip()
            evalue = cols[2].text.strip()
            range_ = cols[3].text.strip()
            family = cols[4].a.text.strip() if cols[4].a else cols[4].text.strip()
            
            data.append([species, protein_id, evalue, range_, family])
        
        df = pd.DataFrame(data, columns=["Species", "Protein_ID", "E-value", "Range", "Family"])
        print("SUPERFAMILY:", value)
        print(type(df))
        value = value.replace("\n", "")
        df.to_csv(f"{value}_table.csv")