import pymongo
from pymongo import MongoClient
from PIL import Image
import urllib
import os
import shutil

Image.MAX_IMAGE_PIXELS = None


client = MongoClient('localhost', 27017)

db = client.crawler

collection = db.twitter

for line in collection.find().sort("num", pymongo.DESCENDING).limit(500):
	name=line["_id"]
	try:
		im = Image.open('/home/my/storage/twitter/'+name)
	except IOError:
		shutil.copy('/home/my/storage/twitter/'+name, '/home/my/storage/twitter_thumb/'+name)
		continue
	width = (im.width)/4
	height = (im.height)/4  
	if width>400: 	
		width=400 
	elif width<250:
		width=250
	if height>400:
		height=400
	elif height<250:
		height=250
	
	size = (width,height)
	try:
		if (os.path.exists('/home/my/storage/twitter_thumb/'+name)):
			pass
		else:
			im.thumbnail(size)
			save_path='/home/my/storage/twitter_thumb/'+name+'.'+im.format
			im.save(save_path)
			os.rename(save_path, '/home/my/storage/twitter_thumb/'+name)
	except ValueError:
		shutil.copy('/home/my/storage/twitter/'+name, '/home/my/storage/twitter_thumb/'+name)


client.close()
