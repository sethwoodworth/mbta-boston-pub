from BeautifulSoup import BeautifulStoneSoup
import urllib
from datetime import datetime,date
import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


#database config

engine = create_engine('sqlite:///talerts.sql')


#put an IF statement around this, how do I check if talerts.sql exists?
metadata = MetaData()
talerts_table = Table('talerts', metadata,
    Column('id', Integer, primary_key=True),
    Column('guid', String),
    Column('title', String),
    Column('content', String),
    Column('mbta_date', Date),
    Column('insert_date', Date)
)

metadata.create_all(engine) 

class Talert(object):
    def __init__(self, guid, title, content, mbta_date, insert_date):
        self.guid = guid
        self.title = title
        self.content = content
        self.mbta_date = mbta_date
        self.insert_date = insert_date

    def __repr__(self):
        return "<Talert('%s','%s','%s','%s','%s')>" % (self.guid, self.title, self.content, self.mbta_date, self.insert_date)


Base = declarative_base()

class Talert(Base):
	__tablename__ = 'talerts'

	id = Column(Integer, primary_key=True)
	guid = Column(String)
	title = Column(String)
	content = Column(String)
	mbta_date = Column(DateTime)
	timestamp = Column(DateTime)

	def __init__(self, guid, title, content, mbta_date, insert_date):
		self.guid = guid
		self.title = title
		self.content = content
		self.mbta_date = mbta_date
		self.timetamp = insert_date

	def __repr__(self):
		return "<Talert('%s','%s')>" % (self.guid, self.title)



#setup the feed for Soup
url = 'http://talerts.com/rssfeed/alertsrss.aspx'
response = urllib.urlopen(url)
raw_xml = response.read()
xmlSoup = BeautifulStoneSoup(raw_xml)

#print  xmlSoup.prettify()


def parse_item(item):
	#Return the elements of the items
	guid = item.find("guid").find(text=True)
	date_str = item.find("pubdate").find(text=True)
	title = item.find("title").find(text=True)
	content = item.find("description").find(text=True)
	
	date_format = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
	date = time.mktime(date_format.timetuple())

	return {'guid':guid,
			'title':title,
			'content':content,
			'date':date
			}

def item_block(soup):
	#Take xml and generate items
	for ch in soup.findAll('item'):
		print parse_item(ch)


#item_block(xmlSoup)
