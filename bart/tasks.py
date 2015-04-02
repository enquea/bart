from __future__ import absolute_import

from celery import shared_task
from django.conf import settings

@shared_task
def get_bart_api_data(station_abbr):
    import requests

    BART_API_ROOT = 'http://api.bart.gov/api/etd.aspx'

    params = {
        'cmd': 'etd',
        'orig': station_abbr,
        'key': settings.BART_API_KEY,
    }

    content = requests.get(BART_API_ROOT, params=params).content

    return content
