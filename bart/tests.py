from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from views import get_closest_station


class BartAPITests(APITestCase):
    fixtures = ['stations']

    def setUp(self):
        self.url = reverse('api')
        self.factory = APIRequestFactory()
        self.stations = {
            'oakland_12': {'lat':37.803664, 'long':-122.271604},
            'millbrae': {'lat':37.599787, 'long':-122.38666},
            'fremont': {'lat':37.557355, 'long':-121.9764},
        }

    def test_closest_station_finds_12_street(self):
        station = self.stations['oakland_12']
        request = self.factory.get(self.url, station)
        station = get_closest_station(request) 
        self.assertEqual(station.abbr, '12TH')

    def test_closest_station_finds_millbrae(self):
        station = self.stations['millbrae']
        request = self.factory.get(self.url, station)
        station = get_closest_station(request) 
        self.assertEqual(station.abbr, 'MLBR')

    def test_closest_station_finds_fremont(self):
        station = self.stations['fremont']
        request = self.factory.get(self.url, station)
        station = get_closest_station(request) 
        self.assertEqual(station.abbr, 'FRMT')       

    def test_get_api_data(self):
        station = self.stations['oakland_12']
        response = self.client.get(self.url, station)
        self.assertEqual(response.data[0]['location'], '12th St. Oakland City Center')
