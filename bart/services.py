from models import Station, ETD
from xml.etree import ElementTree


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
            try:
                minutes = float(est.find('minutes').text)
            except ValueError:
                minutes = 0
            direction = est.find('direction').text[0]

            new_etd = ETD(
                destination=destination,
                minutes=minutes,
                direction=direction
            )

            new_etds.append(new_etd)

    return new_etds
