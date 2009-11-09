import urllib
from BeautifulSoup import BeautifulStoneSoup

url = 'http://talerts.com/rssfeed/alertsrss.aspx'
response = urllib.urlopen(url)
raw_xml = response.read()
xmlSoup = BeautifulStoneSoup(raw_xml)

print  xmlSoup.prettify()
