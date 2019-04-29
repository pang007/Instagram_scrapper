from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import requests
import re
import random
import csv

class IGScrapper:
	def __init__(self, username, password, filename, driver_type):
		self.username = username
		self.password = password
		self.filename = filename + '.csv'
		if driver_type.lower() == 'chrome':
			self.driver = webdriver.Chrome() #rmb to download the chromedriver.exe
		elif driver_type.lower() == 'firefox':
			self.driver = webdriver.Firefox() # rmb to download the firefox.exe
		else:
			raise KeyError('the driver_type can only be chrome or firefox!')
		self.instagram_base_url = "https://www.instagram.com/"

	def login(self):
		'''
		This is to use selenium to minmic a human log in process
		sleep is required to ensure there is sufficient time for the browser to load the page and render the content

		'''
		self.driver.get(self.instagram_base_url)
		time.sleep(2)

		try:
			Login_link = self.driver.find_element_by_link_text('Log in')
			Login_link.click()
		except Exception:
			print('Cannot locate the link text login')

		time.sleep(2)

		try:
			username_box = self.driver.find_element_by_xpath("//span[@id='react-root']//div[@class='f0n8F ']/input[@class='_2hvTZ pexuQ zyHYP']")
			username_box.send_keys(username)
			password_box = self.driver.find_element_by_xpath("//span[@id='react-root']//div[@class='f0n8F ']/input[@class='_2hvTZ pexuQ zyHYP']")
			password_box.send_keys(password)
		except Exception:
			print("Cannot find the username/ password box")

		password_box.submit()
		time.sleep(2)

		# close the "Turn on Notification" if any by clicking Not Now
		# if not, then skip
		try:
			self.driver.find_element_by_xpath("//div[@class='RnEpo Yx5HN   ']//div[@class='mt3GC']/button[@class='aOOlW   HoLwm ']").click()
		except Exception:
			pass

	def scrap_photo_link(self):
		'''
		scrap the photo link photo link in the profile page
		input: the beautiful soup object of the designated profile link
		out: the list that contains all photo website link suffix
		'''
		last_height = self.driver.execute_script("return document.body.scrollHeight")
		photo_link = []
		while True:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			soup = BeautifulSoup(self.driver.page_source, 'lxml')
			href_list = soup.find_all('div', {'class': 'Nnq7C weEfm'})
			for href in href_list:
				# Each instagram row has 3 photo link
				for i in range(3):
					# try except is to avoid error occurs when there is less than 3 link in the instragram row at the end
					try:
						href_item = href.find_all('a', href=True)[i]['href']
						if href_item not in photo_link:
							photo_link.append(href_item)
					except IndexError:
						pass
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height

		print('{} numbers of photo link is extracted'.format(len(photo_link)))
		return photo_link


	def scrap_profile(self, username):
		'''
		function to scrap num of post, followers and following 
		input: username
		output: number of post, number of follower, number of following the profile owner has

		'''
		self.driver.get(self.instagram_base_url + username)
		soup = BeautifulSoup(self.driver.page_source, 'lxml')
		# the first 3 list item in ig is the post, follower and following number
		list_item = soup.find_all('li')
		num_post = self.formatting_ig_profile_info(list_item[0].text)
		num_of_follower = self.formatting_ig_profile_info(list_item[1].text)
		num_of_following = self.formatting_ig_profile_info(list_item[2].text)
		photo_link = self.scrap_photo_link()
		return num_post, num_of_follower, num_of_following, photo_link

	def scrap_img_link(self,soup):
		''' 
		Scrap the image link in the post
		input: the beautiful soup object of the designated post
		output: image link 
		'''
		return soup.find_all('img')[1]['src']

	def scrap_post_like(self, soup):
		''' 
		Scrap the number of like in our post
		input: the beautiful soup object of the designated post
		output: num of like of the post
		'''
		post_like_scrapper = soup.find_all('a', {'class':'zV_Nj'})
		n = len(post_like_scrapper)
		if n == 0:
			num_post_like = 0
		elif n == 1:
			num_post_like = post_like_scrapper[0].text
			num_post_like = self.formatting_ig_profile_info(num_post_like)
		else:
			num_post_like = post_like_scrapper[1].text
			num_post_like = self.formatting_ig_profile_info(num_post_like)
		
		return num_post_like

	def scrap_post_datetime(self,soup):
		'''
		Scrap post date
		input: the beautiful soup object of the designated post
		output: date and time fo the post

		'''
		post_datetime_scrapper = soup.find_all('a', {'class':'c-Yi7'})
		post_date = re.search('[0-9]{4}.[0-9]{2}.[0-9]{2}', str(post_datetime_scrapper)).group(0)
		post_time = re.search('[0-9]{2}:[0-9]{2}', str(post_datetime_scrapper)).group(0)
		return post_date, post_time

	def scrap_info_post_by_post(self,  post_link):
		'''
		to intake a list of link of IG
		to scrap the post data one by one

		'''
		post_detail = []
		for link in post_link:
			self.driver.get(self.instagram_base_url + link)
			soup = BeautifulSoup(self.driver.page_source, 'lxml')
			img_link = self.scrap_img_link(soup)
			num_post_like = self.scrap_post_like(soup)
			post_date, post_time = self.scrap_post_datetime(soup)
			post_detail.append((link, img_link, num_post_like, post_date, post_time))
			time.sleep(random.choice([1,2]))
		return post_detail

	def scrap_img_profile(self, username):
		'''
		This is a function to scrap all the img link from the user instagram profile
		'''

		self.driver.get(self.instagram_base_url + username)
		last_height = self.driver.execute_script("return document.body.scrollHeight")
		profile_img = []
		while True:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			soup = BeautifulSoup(self.driver.page_source, 'lxml')
			img_link = soup.find_all('img')
			for i in img_link:
				if i['src'] not in profile_img:
					profile_img.append(i['src'])

			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height

			print("{} numbers of post is extracted!".format(len(profile_img)))
			return profile_img


	def scrap_all_post_info(self, username):
		'''
		To scrap user's all post's post_link, img_like, like, date & time
		and export the result into a csv file in the existing dir

		'''
		self.login()
		num_post, num_of_follower, num_of_following, photo_link = self.scrap_profile(username)
		post_detail = lentaa.scrap_info_post_by_post(photo_link)
		with open(self.filename + '_' + username + '.csv', 'a') as csvFile:
			fields = ['website_link', 'photo_link', 'number_of_like', 'date', 'time']
			writer = csv.writer(csvFile)
			writer.writerow(fields)
			for item in post_detail:
				writer.writerow(item)

	@staticmethod
	def formatting_ig_profile_info(data):
		'''
		function to format the data by extracting the figures and converting k/m in to 1000 and 1000000
		and removing the words such as like after the number
		'''
		data = data.replace('k', '000').replace('m', '000000')
		data = re.search('^[0-9]+', data).group(0)
		return data

if __name__ == "__main__":

	username = '<username input>'
	password = '<passowrd input>'
	filename = 'ig_scrapper'
	driver_type = 'chrome'
	username_to_be_scrapped = '<username to be scrapped>'
	lentaa = IGScrapper(username, password, filename, driver_type)
	lentaa.scrap_all_post_info(username_to_be_scrapped)





