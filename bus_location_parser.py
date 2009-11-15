from BeautifulSoup import BeautifulStoneSoup
import urllib
import urllib2
from datetime import datetime,date
import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import exceptions

#TODO: shouldn't need the import * if I declare what I need below

# database config
engine = create_engine('sqlite:///locations.sql')

# pull metadata if exists
metadata = MetaData(engine)

# creates the table
vehicle_table = Table('vehicles', metadata,
    Column('id', Integer, primary_key=True),
    Column('bus_id', Integer), # mbta's 'id'
    Column('routeTag', Text),
    Column('dirTag', Text), # 'in', 'out', and 'null'
    Column('lat', Float),
    Column('long', Float),
    Column('secsSinceReport', Integer),
    Column('predictable', Boolean),  # can request time to next stop
    Column('heading', Integer),
    Column('lastTime', DateTime),
    Column('timestamp', DateTime)
)

try:
    vehicle_table.create()
except:
    print 'TABLE \'vehicle_table\' already exists'

# Load defs from db if exists for mapping
vehicle_table = Table('vehicles', metadata, autoload=True)

# create a holding class
class Vehicle(object):

    def __repr__(self):
        return '%s(%r,%r)' % (self.__class__.__name__, self.bus_id, self.routeTag, self.lat, self.long, self.lastTime)

# Map holding class to the table def
mapper(Vehicle, vehicle_table)


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
