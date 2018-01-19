# -*- coding: utf-8 -*-
# image_spider.py
# https://doc.scrapy.org/en/latest/intro/tutorial.html
import sys
import os
import urllib
import hashlib
import time
import configparser
from pymongo import MongoClient
from selenium import webdriver
import scrapy

Config = configparser.ConfigParser()

Config.read('./setting.conf')
keyword = Config.get('twitter', 'keyword')
page = Config.get('twitter', 'page')
rootpath= Config.get('twitter', 'rootPath')

options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")

driver = webdriver.Chrome(rootpath+'chromedriver', chrome_options=options)

driver.implicitly_wait(3)
cnt = 0


class ImageSpider(scrapy.Spider):
	name = "twitter"
	def start_requests(self):
		urls = ['https://twitter.com/search?q='+keyword+'&src=typd&lang=ko&max_position=']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		driver.get(response.url)
		#static img
		for link in driver.find_elements_by_css_selector('div.js-adaptive-photo'):
			next_post = link.get_attribute('data-image-url')
			client = MongoClient('localhost', 27017)
			db = client.crawler
			collection = db.drop
			flag = collection.find({"_id": next_post}).count()
			if(flag == 1):
				print next_post
				pass
			else:
				collection.insert({"_id": next_post, "num": int(time.time() * 1000)})
				yield scrapy.Request(next_post, callback=self.parse_img)
			client.close()

		#gif
		for link in driver.find_elements_by_css_selector('div.PlayableMedia-player video'):
			next_post = link.get_attribute('src')
			client = MongoClient('localhost', 27017)
			db = client.crawler
			collection = db.drop
			flag = collection.find({"_id": next_post}).count()
			if(flag == 1):
				print next_post
				pass
			else:
				collection.insert({"_id": next_post, "num": int(time.time() * 1000)})
				yield scrapy.Request(next_post, callback=self.parse_img)
			client.close()
		global cnt
		global page
		cnt += 1
		if cnt >= int(page):
			driver.quit()
			sys.exit()
		min_position = str(driver.find_element_by_css_selector('div.stream-container').get_attribute('data-min-position'))
		print response.url
		url = response.url.split('&max_position')[0] + '&max_position=' + min_position
		yield scrapy.Request(url, callback=self.parse)

	def parse_img(self, response):
		img = response.url
		num = int(time.time() * 1000)
		if img is not None:
			tmp = img
			name = tmp.split('/')[4]
			ext = tmp.split(".")[3]
			self.log(tmp)
			file_path = "%s%s" % (rootpath+"storage/tmp/", name)
			if not(os.path.exists(file_path)):
				urllib.urlretrieve(tmp, file_path)
				f = open(file_path, 'rb')
				hash_name = hashlib.md5(f.read()).hexdigest()
				hash_path = "%s%s" % (rootpath+"storage/twitter/", hash_name)
				if(os.path.exists(hash_path)):
					os.remove(file_path)
				else:
					os.rename(file_path, hash_path)
					yield {
						'_id': hash_name,
						'num': num,
						'ext':ext
					}