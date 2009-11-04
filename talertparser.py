from BeautifulSoup import BeautifulStoneSoup
import urllib
from datetime import datetime,time,date

url = 'http://talerts.com/rssfeed/alertsrss.aspx'
response = urllib.urlopen(url)
raw_xml = response.read()
xmlSoup = BeautifulStoneSoup(raw_xml)

print  BeautifulStoneSoup(raw_xml).pretify()


def parse_entry(entry):
    """Should return: posted date, author, content, permalink, entryid"""
    entryid = entry.get("id")
    permalink = entry.find("a",{"class":"permalink"}).get("href")
    byline = entry.find("span",{"class":"byline"})
    author = byline.find("a").string
    byline_str = str(byline)
    date_str = byline_str[byline_str.find("</a>,")+6 : byline_str.find("M\n")+1].replace("  "," ")

    date = datetime.strptime(date_str, '%B %d, %Y %I:%M %p')

    content = str(entry.find("div",{"class":"entry-body"}))

    return {'author':author,
            'date':date,
            'entryid':entryid,
            'permalink':permalink,
            'content':content
            }


def parse_item(item):
	"""Return the elements of the items"""
	guid = item.get("guid")
	date_str = item.get("pubdate")
	title = item.get("title")
	desc = item.get("description")
	
	date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')

	return {'guid':guid,
			'title':title,
			'desc':desc,
			'date':date
			}

def item_block(raw_xml):
	"""Take xml and generate items"""
	for item in xmlSoup.item:
		parse_item(item)
