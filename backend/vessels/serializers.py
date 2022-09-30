from rest_framework import serializers
from .serializers import *
from .models import Vessel

class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = (
            'id' ,
            'vessel_id',
            'geo_location',
        )
