from BeautifulSoup import BeautifulStoneSoup
import urllib


url = 'http://talerts.com/rssfeed/alertsrss.aspx'
response = urllib.urlopen(url)
raw_xml = response.read()

print  BeautifulStoneSoup(raw_xml).pretify()

