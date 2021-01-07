import requests
import json
import os
import dictionaryMaker
from datetime import date


FILENAME = './data/'

nepsejson = requests.get("https://nepse-data-api.herokuapp.com/data/todaysprice")
nepsejson = nepsejson.json()

def choices():
	print("------Welcome------")
	print("1.To make a new portofolio")
	print("2.To calculate the results")
	print("3.Exit")

class RedditGame:

	def __init__(self):
		pass

	def __get_source_code(self,url):
		url = url + '.json'
		r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
		return r.json()

	def _usernames(self,url):
		username_list = []
		r = self.__get_source_code(url)
		for each_dict in r:
			for items in each_dict['data']['children']:
				for keys in items['data']:
					if keys == "author":
						username_list.append(items['data']['author'])
		username_list.pop(0)
		return username_list

	def _comments(self,url):
		comments_list = []
		r = self.__get_source_code(url)
		for each_dict in r:
			for items in each_dict['data']['children']:
				for keys in items['data']:
					if keys == "body":
						comments_list.append(items['data']['body'])
		return comments_list

	def is_ticker_symbol(self,string):
		company_name = dictionaryMaker.ticker_and_company.get(string,0)
		for each_dict in nepsejson:
			if each_dict['companyName'] == company_name:
				return True

	def make_portofolio(self):
		today = date.today()
		d1 = today.strftime("%Y_%m_%d")
		d1 = d1.replace('/'," ")
		temp = []
		url = input("Please type the url of the reddit post: ")
		usernames = self._usernames(url)
		comments = self._comments(url)

		for i in range(len(usernames)):
			list_for_stocks = []
			dict_for_holdings = {}
			item_data = {}
			# 1. storing username in json
			item_data['user'] = usernames[i]

			# 2.  storing comment in json
			item_data['comment'] = comments[i]

			# 3. storing stocks in json
			# Getting Ticker Symbol inside comment
			for word in comments[i].split():
				if self.is_ticker_symbol(word):
					list_for_stocks.append(word)
			item_data['stocks'] = list_for_stocks

			# 4. storing holdings in json
			for money in comments[i].split():
				if money.isnumeric():
					holdings = int(money)/int(dictionaryMaker.ticker_and_ltp.get(ticker,0))
					dict_for_holdings[ticker] = holdings
				else:
					ticker = money
			item_data['holdings'] = dict_for_holdings
			temp.append(item_data)


		#opening file and packing
		with open(FILENAME+'portofolio_'+d1+'.json','w') as f:
			json.dump(temp,f,indent=4)

	def calculate(self):
		i = 1
		entries = os.listdir("./data")
		file_dict = {}
		for file in entries:
			if not file.startswith("portofolio"): continue
			print(f'{i}) {file}')
			file_dict[i] = file
			i+=1
		file_num = int(input("Please enter the number beside the file: "))
		file = file_dict.get(file_num, 0)
		print(file)
		file = './data/' + file

		with open(file, 'r') as f:
			temp = json.load(f)
		new_temp = []
		os.system('python WritingToExcel.py')
		for entry in temp:
			item_dict = {}
			username = entry['user']
			holdings = entry['holdings']
			item_dict['Username'] = username
			result = {}
			total = 0
			for k, v in holdings.items():
				new_ltp = dictionaryMaker.ticker_and_ltp[k]
				money = float(new_ltp) * float(v)
				result[k] = money
				total = total + money
			item_dict['result'] = result
			item_dict['total'] = total
			new_temp.append(item_dict)

		with open('./data/results.json', 'w') as f1:
			json.dump(new_temp, f1, indent=4)

if __name__ == '__main__':
	reddit1 = RedditGame()

	while True:
		choices()
		choice = input("Enter Number: ")
		# https://www.reddit.com/r/NepalStock/comments/iwzh0n/weekly_trading_game_test/
		# portofolio2021 01 06.json
		if choice == "1":
			reddit1.make_portofolio()
			print("\nPortofolio successfully made!")
		elif choice == "2":
			reddit1.calculate()
			print("\nCalculated Successfully!")
		elif choice == "3":
			break
		else:
			print("Wrong input")











		
