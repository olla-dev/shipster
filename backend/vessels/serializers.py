import json
from vessels.pagination import ResultPagination
from rest_framework import serializers
from django.core import serializers as core_serializers
from django.core.paginator import Paginator
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .serializers import *
from .models import Location, Vessel

# Features:
# 1. Get all vessel locations
# 2. Get location history for a specific vessel

class LocationGeoPointSerializer(GeoFeatureModelSerializer):
    '''Represents a GeoJson Point Location'''
    class Meta:
        model = Location
        geo_field='point'
        fields = (
            'id',
            'vessel_id',
            'received_time_utc',
        )

class VesselGeoSerializer(serializers.ModelSerializer):
    '''Represents a vessel as a GeoJson Feature'''
    latest_location = serializers.SerializerMethodField()
    journey = serializers.SerializerMethodField()
    
    class Meta:
        model = Vessel
        fields = ('vessel_id', 'latest_location', 'journey')
    
    def get_latest_location(self, obj):
        return LocationGeoPointSerializer(obj.latest_location, many=False).data
    
    def get_journey(self, obj):
        return {
            'type': 'Feature',
            'properties': {},
            'geometry': json.loads(obj.journey.geojson)
        }

class VesselModelSerializer(serializers.ModelSerializer):
    '''Serializes a Vessel and its recorded locations'''
    locations = serializers.SerializerMethodField()
    journey = serializers.SerializerMethodField()

    class Meta:
        model = Vessel
        lookup_field = 'vessel_id'
        fields = ('vessel_id', 'locations', 'journey')
    
    def get_locations(self, obj):
        page_size = ResultPagination.page_size
        paginator = Paginator(
            Location.objects.filter(vessel__vessel_id=obj.vessel_id),
            page_size
        )
        locations = paginator.page(1)
        return LocationGeoPointSerializer(locations, many=True).data
    
    def get_journey(self, obj):
        return obj.journey.json

class CsvModelSerializer(serializers.ModelSerializer):
    '''Serializes all locations as csv rows'''
    vessel_id = serializers.IntegerField(source='vessel.vessel_id')

    class Meta:
        model = Location
        
    def to_representation(self, instance):        
        representation = {
            'received_time_utc': instance.received_time_utc,
            'vessel_id': instance.vessel_id,
            'latitude': instance.point.coords[1],
            'longitude': instance.point.coords[0]
        } 
        return representation