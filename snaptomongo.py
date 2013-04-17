import sys
import os
import ast
import tldextract
import gzip
import pymongo
from pymongo import MongoClient
from datetime import datetime

def main():

	try:
		client = MongoClient()
		db = client.snap
		collection = db.news
	except: #this is lame, fix it
		print 'Mongo problem, is mongod running?'
	
	target_dir = sys.argv[1]

	for item in os.listdir(target_dir):

		item_path = os.path.join(target_dir, item)

		if item.startswith('web-') and item.endswith('.gz'):

			gzfile = gzip.GzipFile(item_path)
			snapfile = gzfile.read()
			snapdocs = [ast.literal_eval(doc) for doc in snapfile.splitlines()]

			print item + ' processed.'

			for doc in snapdocs:
				url = tldextract.extract(doc['url'])
				doc['subdomain'] = url.subdomain
				doc['domain'] = url.domain
				doc['tld'] = url.tld
				doc['date'] = datetime.strptime(doc['date'], '%Y-%m-%d %H:%M:%S')
				collection.insert(doc)

			print item + ' added to database.'
	

if __name__ == "__main__":
	main()
