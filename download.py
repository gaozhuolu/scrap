from pyvirtualdisplay import Display
from selenium import webdriver
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()

import sys

start_index = int(sys.argv[1])


maximumRecords = 15
page_num = 3391

# maximumRecords = 50
# page_num = 1018
# page_num = 3

saveDir = 'temp/page_data'
if not os.path.exists(saveDir):
	os.makedirs(saveDir)

for i in range(start_index, page_num):
	pageurl = "http://gallica.bnf.fr/services/engine/search/sru?operation=searchRetrieve&version=1.2&maximumRecords=" + str(maximumRecords) + "&query=dc.type%20adj%20%22sonore%22%20%20%20sortby%20dc.date%2Fsort.ascending&filter=&page="
	pageurl = pageurl + str(i + 1);

	print 'get: ', pageurl
	driver.get(pageurl)
	delay = 100 # seconds
	try:
		element = WebDriverWait(driver, delay).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '.result-contenu'))
		)
		print 'page is loaded'
	except TimeoutException:
		print "Loading took too much time!"

	html = driver.page_source.encode('utf-8')

	filename = saveDir + '/page' + str(i + 1) + '.txt'
	fh = open(filename, 'w');
	fh.write(html)
	fh.close()
	print 'created file: ', filename
	
driver.quit()
