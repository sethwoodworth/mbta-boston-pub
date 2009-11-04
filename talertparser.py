from BeautifulSoup import BeautifulStoneSoup
import urllib
from datetime import datetime,time,date

url = 'http://talerts.com/rssfeed/alertsrss.aspx'
response = urllib.urlopen(url)
raw_xml = response.read()
xmlSoup = BeautifulStoneSoup(raw_xml)

#print  xmlSoup.prettify()


def parse_item(item):
	"""Return the elements of the items"""
	guid = item.get("guid")
	date_str = item.get("pubdate")
	title = item.get("title")
	desc = item.get("description")
	
#	date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')

	return {'guid':guid,
			'title':title,
			'desc':desc,
			'date':date_str
			}

def item_block(soup):
	"""Take xml and generate items"""
	for ch in soup.findAll('item'):
		print ch.find('guid')


item_block(xmlSoup)
