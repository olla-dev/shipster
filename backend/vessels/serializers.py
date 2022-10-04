import json
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .serializers import *
from .models import Location, Vessel

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

class VesselModelSerializer(serializers.ModelSerializer):
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

class VesselJourneySerializer(serializers.ModelSerializer):
    '''Serializes a Vessel's journey as a LineString'''
    journey = serializers.SerializerMethodField()

    class Meta:
        model = Vessel
        lookup_field = 'vessel_id'
        fields = ('vessel_id', 'journey')
    
    def get_journey(self, obj):
        return {
            'type': 'Feature',
            'properties': {},
            'geometry': json.loads(obj.journey.geojson)
        }

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