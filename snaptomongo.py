import sys
import os
import ast
import collections
import tldextract
import pymongo
from pymongo import MongoClient
import gzip

def domainfilter(urlstring):
	url = tldextract.extract(urlstring)
	print url.subdomain + '.' + url.domain
	
#def newdoc(snapdoc):


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
				print domainfilter(doc['url'])
				collection.insert(doc)

			print item + ' added to database.'
	

if __name__ == "__main__":
	main()
