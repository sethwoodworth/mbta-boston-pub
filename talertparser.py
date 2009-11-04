from BeautifulSoup import BeautifulStoneSoup
import urllib
from datetime import datetime,date
import time

url = 'http://talerts.com/rssfeed/alertsrss.aspx'
response = urllib.urlopen(url)
raw_xml = response.read()
xmlSoup = BeautifulStoneSoup(raw_xml)

#print  xmlSoup.prettify()


def parse_item(item):
	"""Return the elements of the items"""
	guid = item.find("guid").find(text=True)
	date_str = item.find("pubdate").find(text=True)
	title = item.find("title").find(text=True)
	desc = item.find("description").find(text=True)
	
	date_format = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
	date = time.mktime(date_format.timetuple())

	return {'guid':guid,
			'title':title,
			'desc':desc,
			'date':date
			}

def item_block(soup):
	"""Take xml and generate items"""
	for ch in soup.findAll('item'):
		print parse_item(ch)


item_block(xmlSoup)
