import requests
import json
import openpyxl

todays_price = requests.get("https://nepse-data-api.herokuapp.com/data/todaysprice")
data = todays_price.json()

workbook = openpyxl.load_workbook("./data/STONKS V2.5Beta.xlsx")
sheet = workbook.get_sheet_by_name("STONKS")

for i in range(len(data)):
    details = data[i]
    company = details ["companyName"]
    price = details ["closingPrice"]

    for j in range (1,sheet.max_row):
        a = sheet["A"+str(j)]
        c = sheet["C"+str(j)]
        if a.value == company:
            c.value =  price
workbook.save("./data/STONKS V2.5Beta.xlsx")