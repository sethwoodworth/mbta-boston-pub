#!/bin/sh
TIME=`date +%s`

curl "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r=39&t=0" > /pro/boston/bus/data/39.$TIME.xml
sleep 3
curl "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r=111&t=0" > /pro/boston/bus/data/111.$TIME.xml
sleep 3
curl "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r=114&t=0" > /pro/boston/bus/data/114.$TIME.xml
sleep 3
curl "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r=116&t=0" > /pro/boston/bus/data/116.$TIME.xml
sleep 3
curl "http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=mbta&r=117&t=0" > /pro/boston/bus/data/117.$TIME.xml
