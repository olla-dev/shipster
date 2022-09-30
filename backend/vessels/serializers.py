from rest_framework import serializers
from .serializers import *
from .models import Vessel

class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = (
            'id' ,
            'title',
            'type',
            'rating',
            'description',
            'start_date',
            'end_date',
            'geo_location',
            'step_index_in_trip',
            'rating',
            'images'
        )
