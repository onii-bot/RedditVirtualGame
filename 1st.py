import requests
from lxml import html
import json
import openpyxl
import time
import os

timestr = time.strftime("%Y-%m-%d")
extension = ".txt"
file_name =  "Results "+ timestr + extension

def urlGetter():
        """ Gets the latest url of the user"""
        url = 'https://www.reddit.com/user/GameBotNEPSEBETS/'
        url = url + '.json'
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        r = r.json()
        url_list = []
        for items in r["data"]["children"]:
            for keys in items['data']:
                if keys == "permalink":
                    url_list.append(items['data']['permalink'])

        return 'https://www.reddit.com'+url_list[1]
url = urlGetter()
def get_source_code(url):
        """ Makes the url and returns json format of it"""
        url = url + '.json'
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        return r.json()

def usernames(url):
    """ Brings the Usernames from the given url"""
    username_list = []
    r = get_source_code(url)
    for each_dict in r:
        for items in each_dict['data']['children']:
            for keys in items['data']:
                if keys == "author":
                    username_list.append(items['data']['author'])
    username_list.pop(0)
    return username_list

def comments(url):
    """Brings the Comments From given url"""
    comments_list = []
    r = get_source_code(url)
    for each_dict in r:
        for items in each_dict['data']['children']:
            for keys in items['data']:
                if keys == "body":
                    comments_list.append(items['data']['body'])
    return comments_list

sharesansar = requests.get("https://www.sharesansar.com/")
share = html.fromstring(sharesansar.content)
index = share.xpath('//*[@id="as-indices"]/div/table/tbody/tr[1]/td[2]/text()')
index_string = str(index)
index_string = index_string.replace(',','')
index_string = index_string.replace('[','')
index_string = index_string.replace(']','')
index_string = index_string.replace("'","")
index_float = float(index_string)

index_file = open('index.txt','r')
index_fileo = index_file.read()
indexo = float(index_fileo)
index_data = ((index_float-indexo)/indexo)*100
index_datao = round(index_data,2)
index_file.close()

todays_price = requests.get("https://nepse-data-api.herokuapp.com/data/todaysprice")
data = todays_price.json()

#this line is temporary: 
url = 'https://www.reddit.com/r/NEPSEBets/comments/rhnrvp/weekly_trading_game/'

workbook = openpyxl.load_workbook("LTP.xlsx")
sheet = workbook["STONKS"]
sheet = workbook.active
username_lists = usernames(url)
print(username_lists)
comments_lists = comments(url)
#this line is a failsafe: comments_lists = ['JBBL 33% RHPL 34% API 33%', 'BPCL 100%', 'NABIL 30% STC 40% SLI 30%', 'CCBL 100%', 'CHL 40% NBB 10% MHNL 10% JBLB 20% AKPL 20%', 'JBLB 10% KSBBL 20% NHDL 40% RHPL 30%', 'MLBSL 100%']
username_comments = dict()
for i in range(len(username_lists)):
    username_comments[username_lists[i]] = comments_lists[i]
user_portofolio = dict()
t = 0

for j in username_lists:
    total_amount = 0
    holding = username_comments[j]
    holdings = holding.split(" ")
    holdingso = [" ".join(holdings[i:i+2]) for i in range(0, len(holdings), 2)]

    for k in holdingso:
        holdingo = k.split(" ")
        ticker = holdingo[0]
        capital = int(holdingo[1].replace("%",""))

        for l in range (1, sheet.max_row):
            a = sheet["A"+str(l)]
            b = sheet["B"+str(l)]
            c = sheet["C"+str(l)]

            if b.value == ticker:
                companyo = a.value
                no_of_shares = capital/c.value

                for i in range(len(data)):
                    details = data[i]
                    company = details ["companyName"]
                    price = details ["closingPrice"]

                    if companyo == company:
                        total_amount = total_amount + no_of_shares*price

    user_portofolio[username_lists[t]] = round(float(total_amount-100),2)
    t = t + 1

workbook.close()
sorted_user_portofolio = sorted(user_portofolio.items(), key=lambda x: x[1], reverse=True)    
winnerz = str(list(sorted_user_portofolio)[0])
winner = winnerz.split(",")
winnero = str(winner[0]).replace('(','')
winnero = str(winnero.replace("'",''))
output = 'Congratulations to u/' + winnero + ' for winning the weekly trading game with a gain of' + str(winner[1]).replace(')','') + '% .' + 'NEPSE index gained ' + str(index_datao) +'%' +' in the same period. \n' + str(sorted_user_portofolio)
print(output)

directory = os.getcwd()
directory = directory + '\\Results'
os.chdir(directory)
with open(file_name,"w") as f:
    f.write(output)
    f.close()
time.sleep(30)