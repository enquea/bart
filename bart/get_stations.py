import requests

from xml.etree import ElementTree

from models import Station

BART_API_ROOT = 'http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V'
BART_KEY = 'MW9S-E7SL-26DU-VV8V'

response = requests.get(BART_API_ROOT)
root = ElementTree.fromstring(response.content)
stations = root.find('stations').findall('station')
for station in stations:
    name = station.find('name').text
    abbr = station.find('abbr').text
    long = station.find('gtfs_longitude').text
    lat = station.find('gtfs_latitude').text

    Station.objects.get_or_create(
        name=name,
        abbr=abbr,
        long=long,
        lat=lat,
    )
