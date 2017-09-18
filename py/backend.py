
import os
import random
import time
import re
import urllib.robotparser as robotparser
import requests
from bs4 import BeautifulSoup as bsoup



class RequestProxy(object):


	agent_file = (os.path.abspath(
		os.path.join(os.getcwd(), '..', 'data', 'user_agents.txt')))


	def __init__(self):


		self.useragents = self.load_user_agents(RequestProxy.agent_file)
		self.proxy_list = []
		self.get_proxyfor()
		self.get_proxy_us()
	

	def load_user_agents(self, useragentsfile):


		useragents = []

		with open(useragentsfile, 'r') as uaf:
			for ua in uaf:
				if ua:
					useragents.append(ua.strip()[1:-1-1])
		random.shuffle(useragents)
		return useragents


	def get_random_user_agent(self):


		user_agent = random.choice(self.useragents)
		return user_agent


	def get_random_request_headers(self):


		self.headers = {
		"Connection" : "close",
		"User-agent" : self.get_random_user_agent()}
		return self.headers


	def get_proxyfor(self):


		web_url = "http://proxyfor.eu/geo.php"
		self.proxy_list = []
		content = requests.get(web_url).content
		soup = bsoup(content, "html.parser")
		table = soup.find("table", class_="proxy_list")
		
		headings = [th.get_text() for th in table.find("tr").find_all("th")]
		
		datasets = []
		for row in table.find_all("tr")[1:]:

			dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
			datasets.append(dataset)

		for dataset in datasets:
		   # Check Field[0] for tags and field[1] for values!
			proxy = "http://"
			for field in dataset:

				if field[0] == 'IP':
					proxy = proxy+field[1]+':'

				elif field[0] == 'Port':
					proxy = proxy+field[1]

			self.proxy_list.append(proxy)


	def get_proxy_us(self):


		web_url = "https://www.us-proxy.org/"
		content = requests.get(web_url).content
		soup = bsoup(content, 'html.parser')
		table = soup.find('table')

		headers = [th.get_text() for th in table.find('tr').find_all('th')]
		
		datasets = []
		for row in table.find_all('tr')[1:-1]:

			dataset = zip(headers, (td.get_text() for td in row.find_all("td")))
			datasets.append(dataset)

		for dataset in datasets:
			
			# Check Field[0] for tags and field[1] for values!
			proxy = "http://"
			for field in dataset:

				if field[0] == 'IP Address':
					proxy = proxy+field[1]+':'
				
				elif field[0] == 'Port':
					proxy = proxy+field[1]

			self.proxy_list.append(proxy)
		

	def get_random_proxy(self):


		random.shuffle(self.proxy_list)
		req_headers = self.get_random_request_headers()

		return random.choice(self.proxy_list)



class AppRobot(robotparser.RobotFileParser):


	def __init__(self):
		super(AppRobot, self).__init__()


	def check_robots(self, robots_url):

		'''Set the robot parser'''
		self.set_url(robots_url)
		self.read()


	def can_fetch(self, useragent, url):

		'''Check if robot can crawl through the page'''
		return super(AppRobot, self).can_fetch(useragent, url)
		



class WebpageScanner(object):

	base_url = 'https://panoramafirm.pl/'

	def __init__(self):
		#super(WebpageScanner, self).__init__()
		self.main_url = WebpageScanner.base_url


	def get_page_url(self, mthd, webpage, random_agent, random_prox):

			
		time.sleep(10)
		self.proxies = random_prox
		self.headers = random_agent
		print(self.proxies, self.headers)
		return requests.request(
			method=mthd, url=webpage, headers=self.headers,
			proxies={"http:" : self.proxies})


	def category_search(self, category, mthd, webpage, random_agent, random_prox):


		chosen_cat = self.main_url + category.lower().replace(' ', '_')
		return chosen_cat


	def user_search_url(self, first_param, second_param=None, both_params=False):


		'''Create from user-custom search new url to request'''
		
		if both_params:
			
			#if params bool is true, search by type and location
			type_param = 'szukaj?k='+ first_param
			type_param = type_param.lower().replace(' ', '_')
			localisation_param = '&l=' + second_param
			localisation_param = localisation_param.lower().replace(' ', '_')

			#merge base url with parameters
			self.main_url += type_param
			self.main_url += localisation_param
			self.custom_url = base_url
			return self.custom_url

		else:
			
			#bool is false, search by type of company only
			type_param = 'szukaj?k='+ first_param
			type_param = type_param.lower().replace(' ', '_')
			self.main_url += type_param
			self.custom_url = base_url
			return self.custom_url



class SoupWrap(bsoup):

	data = []

	def __init__(self, *args, **kwargs):
		super(SoupWrap, self).__init__(*args, **kwargs)
		
		#data structures for collected data
		#divided_adrs -> divided addresses (town, street)
		#addresses -> undivided addresses
		#categories -> list for built-in categories of search on webpage
		#mails -> list of collected mails
		#companies -> list of companies -> address and mail (nested lists)
		self.divided_adrs = []
		self.addresses = []
		self.categories = []
		self.comp_names = []
		self.mails = []
		self.companies = []
		self.result_count = 0


	def get_categories(self, *args, **kwargs):


		'''Find text in html and store in categories list'''
		([self.categories.append(link.text)
			for link in self.find_all(*args, **kwargs)])


	def send_categories(self):

		return self.categories


	def get_address(self, *args, **kwargs):

		([self.addresses.append(content.text)
			for content in self.find_all(*args, **kwargs)])
			

	def clean_address(self):

		for index, address in enumerate(self.addresses):
			self.addresses[index] = address.strip(" \n\r")


	def split_address(self):

		default = "Brak"

		for index, address in enumerate(self.addresses):
			one_div_adrs = self.addresses[index].split(',')
			if len(one_div_adrs) < 2:
				if len(one_div_adrs) == 0:
					for default in range(2):
						one_div_adrs.insert(0, default)
				else:
					one_div_adrs.insert(0, default)

			
			one_div_adrs.reverse()
			
			for index2, item in enumerate(one_div_adrs):
				one_div_adrs[index2] = one_div_adrs[index2].strip()
			

			self.divided_adrs.append(one_div_adrs)


	def get_comp_name(self, *args, **kwargs):


		([self.comp_names.append(link.text)
				for link in self.find_all(*args, **kwargs)]) 


	def clean_comp_name(self):


		for index, name in enumerate(self.comp_names):
			self.comp_names[index] = name.strip(" \n\r")


	def get_mails(self, parameter, *args, **kwargs):


		([self.mails.append(link.get(parameter))
			for link in self.find_all(*args, **kwargs)])


	def substract_mail(self, nan_msg):


		for index, mail in enumerate(self.mails):

			try:
				found = re.search(r"mailto:(.*)$", mail).group(1)
				
				if found == "":
					found = nan_msg
					
				self.mails[index] = found

			except AttributeError:
				print("Mail not found!")


	def merge_mail_address_name(self):


		for index, address in enumerate(self.divided_adrs):
			self.companies 	= list(self.divided_adrs)
			self.companies[index].append(self.comp_names[index])
			self.companies[index].append(self.mails[index])

		return self.companies



	def category_to_url(self, category, cat_list):


		if category in cat_list:
			self.chosen_category = category.lower().replace(' ', '_')
			return self.chosen_category

		else:
			no_such = "No such string"
			print(no_such)
			return no_such


	def get_num_of_results(self):


		for count in self.find(id="resultCountContainer"):

			self.result_count = int(count.text)


	def is_more(self, tag, param1, param2, pattern):


		for link in self.find_all(tag):
		
			try:
				if link.get(param1) == pattern:
					self.new_url = link.get(param2)
					return True

			except AttributeError:
				print("Nie znaleziono następnej strony!")
				return False