from BeautifulSoup import BeautifulStoneSoup
import urllib


url = 'http://talerts.com/rssfeed/alertsrss.aspx'

response = urllib.urlopen(url)
xml = response.read()
