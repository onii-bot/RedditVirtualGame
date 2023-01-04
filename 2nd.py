import requests
from lxml import html
import json
import openpyxl

sharesansar = requests.get("https://www.sharesansar.com/")
share = html.fromstring(sharesansar.content)
index = share.xpath('//*[@id="as-indices"]/div/table/tbody/tr[1]/td[2]/text()')
index_string = str(index)
index_string = index_string.replace(',','')
index_string = index_string.replace('[','')
index_string = index_string.replace(']','')
index_string = index_string.replace("'","")

with open('index.txt','w') as f:
    f.write(index_string)

todays_price = requests.get("https://nepse-data-api.herokuapp.com/data/todaysprice")
data = todays_price.json()

workbook = openpyxl.load_workbook("LTP.xlsx")
sheet = workbook.get_sheet_by_name("STONKS")

for i in range(len(data)):
    details = data[i]
    company = details ["companyName"]
    price = details ["closingPrice"]

    for j in range (1, sheet.max_row):
        a = sheet["A"+str(j)]
        c = sheet["C"+str(j)]
        if a.value == company:
            print (a.value) 
            print (c.value, price)
            c.value = price
            
workbook.save("LTP.xlsx")