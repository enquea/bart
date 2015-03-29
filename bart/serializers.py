from models import ETD
from rest_framework import serializers


class ETDSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='location.name')
    destination = serializers.CharField(source='destination.name')

    class Meta:
        model = ETD
