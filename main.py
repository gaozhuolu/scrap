import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# activate_env = os.path.expanduser('/newdisk/courtlistener/scraptask/venv/bin/activate_this.py')
# execfile(activate_env, dict(__file__=activate_env))

import re
import uuid
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup

import utils
import dbmodel
# dbuser = 'root'
# dbpasswd = urllib.quote_plus('password')
# client = MongoClient('mongodb://' + dbuser + ':' + dbpasswd + '@localhost')
# db = client.scrapdb

def downloadtest():
	response = urllib2.urlopen('https://www.justice.gov/eoir/page/file/974211/download')
	data = response.read()

	# Write data to file
	file_ = open('download/test.pdf', 'w')
	file_.write(data)
	file_.close()

def downloadFile(url):
	filename = uuid.uuid4()
	try:
		filenumbers = re.findall('\d+', url)
		if len(filenumbers) >= 1:
			filename = filenumbers[len(filenumbers) - 1]
		filename = filename + '.pdf'

		# tmpfile = urllib.URLopener()
		# tmpfile.retrieve(url, 'download/' + filename)
		print url
		response = urllib2.urlopen(url)
		data = response.read()
		 
		# Write data to file
		file_ = open('download/' + filename, 'w')
		file_.write(data)
		file_.close()
	except Exception, e:
		filename = None

	return filename


def scraptest():
	s = requests.Session()
	s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
	# payload = urllib.urlencode({'items': 9999, 'page': 1, 'address1': json_data['straddress'], 'city': json_data['strcity'], 'state': json_data['strstate'], 'zip': json_data['strzip']})
	scrapurls = []
	scrapurls.append('https://www.justice.gov/eoir/volume-27')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-26')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-25')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-24')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-23')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-22')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-21')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-20')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-19')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-18')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-17')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-16')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-15')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-14')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-13')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-12')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-11')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-10')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-09')
	scrapurls.append('https://www.justice.gov/eoir/precedent-decisions-volume-08')

	cnt = 0
	for urlpath in scrapurls:
		r = s.get(urlpath)#, params=payload)
		    
		soup = BeautifulSoup(r.content, 'html.parser')
		roots = soup.find_all('root')
		for root in roots:
			tables = root.find_all('table')
			for table in tables:
				cnt = cnt + 1
				print '---------- Record: ' + str(cnt) + ' -----------------'
				tbody = table.find('tbody')
				tr = tbody.find('tr')
				tds = tr.find_all('td')


				#Name and Date Info
				name = ''
				if len(tds) > 0:
					p = tds[0].find('p')
					if p is None:
						p = tds[0]
					
					tmpstrongs = p.find_all('strong')
					if len(tmpstrongs) == 0:
						tmpstrongs = p.find_all('b')
					
					for v in tmpstrongs:
						try:
							name = name + ' ' + v.string
						except Exception, e:
							pass
					if name != '':
						name = utils.removespecialchars(name)
						#name = re.sub(r'[\xc2]', '', name)
						name = utils.wholerstrip(name, ' ')
						name = utils.wholerstrip(name, '-')
						name = utils.wholerstrip(name, ',')
						name = utils.wholerstrip(name, ' ')

					dateinfo = ''
					if len(tmpstrongs) > 0:
						lastindex = len(tmpstrongs) - 1
						dateinfo = tmpstrongs[lastindex].nextSibling
					if dateinfo != '':
						dateinfo = utils.wholelstrip(dateinfo, ' ')
						dateinfo = utils.wholelstrip(dateinfo, '-')
						dateinfo = utils.wholelstrip(dateinfo, ',')
						dateinfo = utils.wholelstrip(dateinfo, ' ')

				#Download Url
				pdfurl = ''
				if len(tds) > 1:
					ahref = tds[1].find('a')
					if ahref is not None:
						pdfurl = ahref.get('href')
				if 'http' not in pdfurl:
					pdfurl = 'https://www.justice.gov' + pdfurl

				#print 'Name:' + name + '|'
				#print 'Date Info:', dateinfo
				#print 'PDF url:', pdfurl


				#Get Description			
				nextNode = table
				description = ''
				while True:
					if nextNode is None:
						break;
					nextNode = nextNode.nextSibling
					tag_name = ''
					try:
						tag_name = nextNode.name
					except AttributeError:
						tag_name = ''
					if tag_name == 'p':
						tmpstr = ''.join(nextNode.findAll(text=True))
						if tmpstr:
							description = description + ' ' + tmpstr
					if tag_name == 'hr':
						break;
				#print 'Description:', description

				#Download PDF file
				pdfurl = pdfurl.replace('https://justice.gov', 'https://www.justice.gov')
				filename = downloadFile(pdfurl)
				dbmodel.addRecord(name, dateinfo, pdfurl, filename, description)


if __name__ == '__main__':
	scraptest()
	pass
