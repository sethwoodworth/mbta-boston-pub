from BeautifulSoup import BeautifulStoneSoup
import urllib
import urllib2
import re
from datetime import datetime,date
import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

#TODO: shouldn't need the import * if I declare what I need below

# database config
engine = create_engine('sqlite:///bus_locations.sql')

# Instantiates the db #
## TODO: Make this happen as-needed, not every time
## Actually, .create_all(engine) provides this check for me.  This is just a bit messy.

metadata = MetaData()
vehicle = Table('vehicles', metadata,
    Column('id', Integer, primary_key=True),
    Column('bus_id', Integer), # mbta's 'id'
    Column('routeTag', Text),
    Column('dirTag', Text), # 'in', 'out', and 'null'
    Column('lat', Float),
    Column('lon', Float),
    Column('secsSinceReport', Integer),
    Column('predictable', Boolean),  # can request time to next stop
    Column('heading', Integer),
    Column('lastTime', DateTime),
    Column('timestamp', DateTime)
)

metadata.create_all(engine) 
 
# DB Class interactions 
Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True),
    bus_id = Column(Integer), # mbta's 'id'
    routeTag = Column(Text),
    dirTag = Column(Text), # 'in', 'out', and 'null'
    lat = Column(Float),
    long = Column(Float),
    secsSinceReport = Column(Integer),
    predictable = Column(Boolean),  # can request time to next stop
    heading = Column(Integer),
    lastTime = Column(DateTime),
    timestamp = Column(DateTime)

    def __init__(self, bus_id, routeTag, dirTag, lat, long, secsSincneReport, predictable, heading, lastTime, timestamp):

        self.bus_id = bus_id
        self.routeTag = routeTag
        self.dirTag = dirTag
        self.lat = lat
        self.long = long
        self.secsSinceReport = secsSinceReport
        self.predictable = predictable
        self.heading = heading
        self.lastTime = lastTime
        self.timestamp = timestamp

    def __repr__(self):
        return "<Vehicle('%s','%s','%s','%s','%s')>" % (self.bus_id, self.routeTag, self.lat, self.long, self.lastTime)

    def bus_id(self):
        return self.bus_id

Session = sessionmaker(bind=engine)
session = Session()

# Grabbing route information
print 'Pulling the list of NextBus feeds and making Soup'

url_pre = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r='
url_post = '&t=0' # is this needed?
route_number = [39, 111, 114, 116, 117]
route_dict = {}

def soup_bus(route):
    url = url_pre + str(route) + url_post
    response = urllib.urlopen(url)
    raw_xml = response.read()
    return BeautifulStoneSoup(raw_xml)

def soup_store():
    for r in route_number:
        route_dict[r] = soup_bus(r)
    
soup_store()

def parse_location(bus):
    # parse the attributes of the vehicle tag, store for db insert
    #bus_id = item.find("id").find(text=True)))
    #date_raw = item.find("pubdate").find(text=True)
    #title = item.find("title").find(text=True)
    #content = item.find("description").find(text=True)
    
    # MBTA's date format is odd, convert to Unix time then to ISO standard
    #date_str = time.strptime(date_raw, '%a, %d %b %Y %H:%M:%S GMT')
    #date = time.strftime("%Y-%m-%d %H:%M:%S", date_str)
    #cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	#cur_time = datetime.now()

    return bus 

def route_to_bus(soup):
    # Take xml and generate items to be inserted
    for bus in soup.findAll('vehicle'):
        to_add = parse_location(bus)
        session.add(to_add)
    print 'Good, got it, storing now'
    session.commit()

def store_routes():
    for r in route_number:
        page = route_dict[r]
        route_to_bus(page)

store_routes()
