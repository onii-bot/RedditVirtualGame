import requests
import json
import os
from data import dictionaryMaker
from datetime import date
import operator
from lxml import html

FILENAME = './data/'

nepsejson = requests.get("https://nepse-data-api.herokuapp.com/data/todaysprice")
nepsejson = nepsejson.json()

today = date.today()
datetoday = today.strftime("%Y_%m_%d")
datetoday = datetoday.replace('/'," ")
datetoday = 'portofolio_'+datetoday+'.json'

class RedditGame:

	def __init__(self):
		pass

	def __get_source_code(self,url):
		""" Makes the url and returns json format of it"""
		url = url + '.json'
		r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
		return r.json()

	def _usernames(self,url):
		""" Brings the Usernames from the given url"""
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
		"""Brings the Comments From given url"""
		comments_list = []
		r = self.__get_source_code(url)
		for each_dict in r:
			for items in each_dict['data']['children']:
				for keys in items['data']:
					if keys == "body":
						comments_list.append(items['data']['body'])
		return comments_list

	def isTickerSymbol(self,string):
		string = string.upper()
		company_name = dictionaryMaker.ticker_and_company.get(string,0)
		for each_dict in nepsejson:
			if each_dict['companyName'] == company_name:
				return True

	def makePortofolio(self,url):
		"""Makes a portofolio with the date as filename"""
		temp = []
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
				if self.isTickerSymbol(word):
					list_for_stocks.append(word)
			item_data['stocks'] = list_for_stocks

			# 4. storing holdings in json
			for money in comments[i].split():
				if money.isnumeric():
					holdings = int(money)/int(dictionaryMaker.ticker_and_ltp.get(ticker,0))
					dict_for_holdings[ticker] = holdings
				else:
					ticker = money.upper()
			item_data['holdings'] = dict_for_holdings
			temp.append(item_data)


		# opening file and packing
		with open(FILENAME + datetoday,'w') as f:
			json.dump(temp,f,indent=4)

	def calculate(self):
		""" Calculates the portofolio and returns a json"""

		file = './data/'+ datetoday

		with open(file, 'r') as f:
			temp = json.load(f)
		new_temp = []
		os.system('python ./data/WritingToExcel.py')
		from data import dictionaryMaker2
		for entry in temp:
			item_dict = {}
			username = entry['user']
			holdings = entry['holdings']
			item_dict['Username'] = username
			result = {}
			total = 0
			for k, v in holdings.items():
				new_ltp = dictionaryMaker2.ticker_and_ltp[k]
				money = float(new_ltp) * float(v)
				result[k] = money
				total = total + money
			item_dict['result'] = result
			item_dict['total'] = total
			new_temp.append(item_dict)

		with open('./data/results.json', 'w') as f1:
			json.dump(new_temp, f1, indent=4)
		self.sort_and_txt('./data/results.json')
	@staticmethod
	def mepse_index():
		sharesansar = requests.get("https://www.sharesansar.com/")
		share = html.fromstring(sharesansar.content)

		index = share.xpath('//*[@id="as-indices"]/div/table/tbody/tr[1]/td[2]/text()')
		return str(index)

	@staticmethod
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

	@staticmethod
	def sort_and_txt(jsonfile):
		with open(jsonfile) as file:
			data = json.load(file)
			data.sort(key=operator.itemgetter('total'), reverse=True)
			print(data)
		outfile = open('finalresult.txt', 'w')
		for i in range(len(data)):
			details = data[i]
			outfile.write(details["Username"])
			outfile.write("\n")
			outfile.write(str((details["result"])))
			outfile.write("\n")
			outfile.write(str((details["total"])))
			outfile.write("\n")
			outfile.write("\n")

		outfile.close()
		
		fp = open('nepseindex.txt','w')
		fp.write(nepse_index())
		
		fp.close()













		
