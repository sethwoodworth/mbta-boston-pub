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

Session = sessionmaker(bind=engine)
session = Session()

# Grabbing route information
print 'Pulling the list of NextBus feeds and making Soup...'

url_pre = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r='
url_post = '&t=0' # is this needed?
#routeNumber = ['39', '111', '114', '116', '117']
routeNumber = ['39']

Base = declarative_base()
class Vehicle(Base):
    __tablename__ = 'vehicleLocations'

    # <vehicle id="1039" routeTag="39" dirTag="in" lat="42.3011539" lon="-71.1138792" secsSinceReport="31" predictable="true" heading="281"/>

    id      = Column(Integer, primary_key=True)
    vid     = Column("vid", Integer)
    route   = Column("route", String) # Not all routes are ints (CT1, etc.)
    dir     = Column("dir", String) # in, out, null
    lat     = Column("lat", Float)
    lon     = Column("lon", Float)
    time    = Column("time", Integer) 
    # SQLite does not support the datetime object. Store as
    #   seconds from the epoch.
    # Also, this doesn't lock us into one poorly written date/time lib.
    # portability ftw.
    heading = Column(Integer)

    def __init__(self, xmlDesc, tm):
        #vehicle id can be zero padded -- we diregard this
        print xmlDesc.prettify
        self.vid    = int(xmlDesc['id'])
        self.route  = xmlDesc['routetag']
        self.dir    = xmlDesc['dirtag']
        self.lat    = float(xmlDesc['lat'])
        self.lon    = float(xmlDesc['lon'])
        self.time   = (tm - int(xmlDesc['secssincereport'])) # int not datetime
        self.heading = int(xmlDesc['heading']) 

    def __repr__(self):
        return "<Vehicle('%s','%s','%s','%f','%f','%d','%d')>" % (self.vid, self.route, self.dir, self.lat,self.time,self.heading)

# TODO There's no need for mutation of global variables. 
#   Rewrite this code in a more abstract and robust manner.

def storeVehicleData(soup, t):
    # Take xml and generate items to be inserted
    for v in soup.findAll('vehicle'):
        session.add(Vehicle(v,t))
    print 'Good, got it, storing now'
    session.commit()

def storeRoutes(rd):
    for r in rd:
        # NextBus is inconsistent in their tag usage.
        lt = rd[r].find('lastTime')
        if not lt:
            lt = rd[r].find('lasttime')
        tm = int(lt['time'])
        datum = rd[r]
        storeVehicleData(rd[r], tm)

def getRoutes():
    routeDict = {}
    for r in routeNumber:
        resp = urllib2.urlopen(url_pre + r + url_post)
        xm = resp.read()
        routeDict['r'] = BeautifulStoneSoup(xm)
    return routeDict


storeRoutes(getRoutes())
