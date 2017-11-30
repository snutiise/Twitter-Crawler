# image_spider.py 
# https://doc.scrapy.org/en/latest/intro/tutorial.html 

import scrapy 
import sys
import os
import urllib
import urllib2
import hashlib
import time
import pymongo
from pymongo import MongoClient
from selenium import webdriver


token=''
cnt=0
class ImageSpider(scrapy.Spider):
	name = "twitter"
	def start_requests(self):
		urls = ['https://twitter.com?f=tweets&max_position=']
		for url in urls:
			yield scrapy.Request(url=url, cookies={'auth_token':token}, callback=self.parse)
	
	def parse(self, response):
		#for post in response.css('small.time'):
		#	next_post = post.css('a::attr(href)').extract_first() 
		#	if next_post is not None:
		for link in response.css('div.js-adaptive-photo'):
			next_post = link.xpath('@data-image-url').extract()[0]
			client = MongoClient('localhost', 27017)
			db = client.crawler
			collection = db.drop
			flag=collection.find({"_id":next_post}).count()
			#flag=0
			if(flag==1):
				print next_post
				pass
			else:
				collection.insert({"_id":next_post,"num":int(time.time()*1000)})
				#next_post = response.urljoin(next_post) 
				yield scrapy.Request(next_post, cookies={'auth_token':token}, callback=self.parse_img)
			client.close()
		global cnt
		cnt+=1
		if cnt>=10:
			sys.exit()
		min_position = response.css('div.conversations-enabled').xpath('@data-min-position').extract()
		print min_position
		url = response.url.split('max_position')[0]+'max_position='+min_position[0]
		yield scrapy.Request(url, cookies={'auth_token':token}, callback=self.parse)
	def parse_img(self, response):
		img=response.url
		#img_list=''
		#video_list=''
		#for link in response.css('div.js-adaptive-photo'):
		#	img_list = link.xpath('@data-image-url').extract()
                num = int(time.time()*1000)
		
		#for link in response.css('div.AdaptiveMedia-videoContainer'):
		#	video_list = link.css('div.PlayableMedia')
		#	num = int(time.time()*1000)


		#for img in img_list: 
		if img is not None:
			tmp = img
			name = tmp.split('/')[4]
			self.log(tmp)
			file_path = "%s%s" % ("/home/my/storage/tmp/", name)
			if not(os.path.exists(file_path)):
				urllib.urlretrieve(tmp, file_path)
				f = open(file_path, 'rb')
				hash_name = hashlib.md5(f.read()).hexdigest()
				hash_path = "%s%s" % ("/home/my/storage/twitter/", hash_name)
				if(os.path.exists(hash_path)):
					os.remove(file_path)
					#pass
				else :
					os.rename(file_path, hash_path)
					yield {
                              	        	'_id' : hash_name,
                                    		'num' : num
					}
"""
		for video in video_list:
			if video is not None:
				url=url.replace('twitter','mobile.twitter')
				url=url+'/video/1'
				browser = webdriver.PhantomJS()
				#browser.delete_all_cookies()
				#browser.add_cookie({'domain':'.twitter.com','name':'auth_token','value':token,'path':'/','expires':None})
				browser.get(url)
				print url
				browser.implicitly_wait(10)
				tmp = browser.find_element_by_css_selector('body').get_attribute('innerHTML')
				print tmp
				browser.quit()
				tmp=tmp.split('<source')[1]
				tmp=tmp.split('\"')[1]
				self.log(tmp)
				file_path = "%s%s" % ("/home/my/storage/tmp/", num)
				if not(os.path.exists(file_path)):
					urllib.urlretrieve(tmp, file_path)
					f = open(file_path, 'rb')
					hash_name = hashlib.md5(f.read()).hexdigest()
					hash_path = "%s%s" % ("/home/my/storage/twitter/", hash_name)
					if(os.path.exists(hash_path)):
						os.remove(file_path)
					else :
						os.rename(file_path, hash_path)
						yield{
							'_id' : hash_name,
							'type' : 'video',
							'num' : num
						}
				
"""


