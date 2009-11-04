from BeautifulSoup import BeautifulStoneSoup
import urllib
from datetime import datetime,date
import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#database config
engine = create_engine('sqlite:///talerts.sql')

#Instantiates the db
#TODO: Make this happen as-needed, not every time
metadata = MetaData()
talerts_table = Table('talerts', metadata,
    Column('id', Integer, primary_key=True),
    Column('guid', String),
    Column('title', String),
    Column('content', String),
    Column('mbta_date', DateTime),
    Column('timestamp', DateTime)
)
metadata.create_all(engine) 
 
#sets up future db interactions 
Base = declarative_base()

class Talert(Base):
	__tablename__ = 'talerts'

	id = Column(Integer, primary_key=True)
	guid = Column(String)
	title = Column(String)
	content = Column(String)
	mbta_date = Column(DateTime)
	timestamp = Column(DateTime)

	def __init__(self, guid, title, content, mbta_date, timestamp):
		self.guid = guid
		self.title = title
		self.content = content
		self.mbta_date = mbta_date
		self.timestamp = timestamp

	def __repr__(self):
		return "<Talert('%s','%s','%s','%s','%s')>" % (self.guid, self.title, self.content, self.mbta_date, self.timestamp)
		

Session = sessionmaker(bind=engine)
session = Session()

ta1 = Talert('guid1234','title4321','somecontent','200911040000','200911040001')


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
	cur_time = time.time()

	return {'guid':guid,
			'title':title,
			'content':content,
			'date':date,
			'cur_time':cur_time
			}

def item_block(soup):
	#Take xml and generate items
	for ch in soup.findAll('item'):
		print parse_item(ch)


item_block(xmlSoup)
