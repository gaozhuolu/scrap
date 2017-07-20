import os
import sys
import datetime
import urllib
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')



dbuser = 'root'
dbpasswd = urllib.quote_plus('password')
# client = MongoClient('mongodb://' + dbuser + ':' + dbpasswd + '@localhost:27017')
client = MongoClient('mongodb://localhost:27017')
db = client.scrapdb

def addRecord(name, dateinfo, pdfurl, filename):
	_id = db.datum.insert({
		'name': name,
		'dateinfo': dateinfo,
		'pdfurl': pdfurl,
		'filename': filename,
		'dateadded': datetime.datetime.utcnow()
		})