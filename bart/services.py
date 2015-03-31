import math
import requests

from django.conf import settings
from django.utils import timezone
from models import Station, ETD
from xml.etree import ElementTree


def get_line_dist(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
  

def get_closest_station(request):
    """
    Based on user geolocation
    Get closest station by Euclidean distance

    Maybe better to use GEODjango
    Or
    Store threshhold coordinates and directly map to station
    """
    user_long = float(request.GET['long'])
    user_lat = float(request.GET['lat'])

    stations = Station.objects.all()
    min_dist = 2**64
    closest_station = None
    for station in stations:
        station_location = (station.long, station.lat)
        user_location = (user_long, user_lat)
        dist = get_line_dist(station_location, user_location) 
        if dist < min_dist:
            min_dist = dist
            closest_station = station

    return closest_station                

def get_time_to_depart(minutes):
    """
    Convert XML minutes string to time to depart
    """
    try:
        minutes = int(minutes)
    except ValueError:
        minutes = 0

    return timezone.now() + timezone.timedelta(minutes=minutes)

def get_new_etds(bart_data):
    """
    Convert ETD XML data and push into DB
    """
    new_etds = []

    root = ElementTree.fromstring(bart_data.content)
    etds = root.find('station').findall('etd')
    for etd in etds:
        abbr = etd.find('abbreviation').text
        destination = Station.objects.get(abbr=abbr)
        estimates = etd.findall('estimate')

        for est in estimates:
            time_to_depart = get_time_to_depart(est.find('minutes').text)
            direction = est.find('direction').text[0]

            new_etd = ETD(
                destination=destination,
                time_to_depart=time_to_depart,
                direction=direction
            )

            new_etds.append(new_etd)

    return new_etds


def update_station_data(request, station):
    """
    Update outgoing times from a station based on data from BART API
    Only ask if our data is more than <2> minutes old
    """
    BART_API_ROOT = 'http://api.bart.gov/api/etd.aspx'

    time_since_updated = timezone.now() - station.updated_at
    if time_since_updated.seconds > 120:

        params = {
            'cmd': 'etd',
            'orig': station.abbr.lower(),
            'key': settings.BART_API_KEY,
        }

        data = requests.get(BART_API_ROOT, params=params)
        station.etds_from.all().delete()
        station.etds_from = get_new_etds(data)
        station.save()
