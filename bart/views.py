import math
import requests

from models import Station, ETD
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services import get_new_etds
from serializers import ETDSerializer


def get_line_dist(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
  

def get_closest_station(request):
    """
    Naive solution to get closest station by Euclidean distance
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


def update_station_data(request, station):
    """
    Update outgoing times from a station based on data from BART API
    """
    BART_API_ROOT = 'http://api.bart.gov/api/etd.aspx'
    BART_API_KEY = 'MW9S-E7SL-26DU-VV8V'

    params = {
        'cmd': 'etd',
        'orig': station.abbr.lower(),
        'key': BART_API_KEY,
    }
    data = requests.get(BART_API_ROOT, params=params)
    station.etds_from.all().delete()
    station.etds_from = get_new_etds(data)


@api_view()
def etd_data(request):
    closest_station = get_closest_station(request)

    update_station_data(request, closest_station)

    etds = closest_station.etds_from.all()
    serializer = ETDSerializer(etds, many=True)
    return Response(serializer.data)
