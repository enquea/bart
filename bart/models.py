from django.db import models


class Station(models.Model):
    """
    A physical station (Fremont, Daly City, etc)
    one-to-many with ETDs
    """
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=10)
    long = models.FloatField()
    lat = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


class ETD(models.Model):
    """ 
    Estimated time to departure
    """
    DIRECTIONS = (
        ('N', 'North'),
        ('S', 'South'),
    )

    location = models.ForeignKey('Station', related_name='etds_from')
    destination = models.ForeignKey('Station', related_name='etds_to')
    time_to_depart = models.DateTimeField()
    direction = models.CharField(max_length=1, choices=DIRECTIONS)

