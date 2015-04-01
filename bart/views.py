from django.shortcuts import render_to_response
from models import Station, ETD
from rest_framework.decorators import api_view
from rest_framework.response import Response
from services import get_closest_station, update_station_data 
from serializers import ETDSerializer

def home(request):
    return render_to_response('base.html')

@api_view()
def etd_data(request):
    closest_station = get_closest_station(request)
    update_station_data(closest_station)

    etds = closest_station.etds_from.all()
    serializer = ETDSerializer(etds, many=True)
    return Response(serializer.data)
