from vessels.pagination import ResultPagination
from rest_framework import serializers
from django.core.paginator import Paginator
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .serializers import *
from .models import Location, Vessel

# Features:
# 1. Get all vessel locations
# 2. Get location history for a specific vessel

class LocationGeoPointSerializer(serializers.ModelSerializer):
    '''Represents a GeoJson Point Location'''
    location = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            'id',
            'received_time_utc',
            'point'
        )

    def to_representation(self, instance):
        coordinates = [
            instance.point.coords[0],
            instance.point.coords[1]
        ]
        
        representation = {
            'type': 'Point',
            'coordinates': coordinates
        } 
        return representation

class VesselGeoSerializer(GeoFeatureModelSerializer):
    '''Represents a vessel as a GeoJson Feature'''
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = Vessel
        geo_field = 'location'
        id_field = 'vessel_id'
        fields = ('vessel_id',)
    
    def get_properties(self, instance, fields):
        location = Location.objects.filter(vessel__vessel_id=instance.vessel_id).latest('received_time_utc')
        return {
            'vessel_id': instance.vessel_id, 
            'received_time_utc': location.received_time_utc,
            'latitude': location.point.coords[0],
            'longitude': location.point.coords[1] 
        }
    
    def get_location(self, obj):
        location = Location.objects.filter(vessel__vessel_id=obj.vessel_id).latest('received_time_utc')
        return LocationGeoPointSerializer(location, many=False).data


class LocationModelSerializer(serializers.ModelSerializer):
    '''Simple Location Model Serializer'''
    class Meta:
        model = Location
        fields = (
            'id',
            'received_time_utc',
            'point',
        )

class VesselModelSerializer(serializers.ModelSerializer):
    '''Serializes a Vessel and its recorded locations'''
    locations = serializers.SerializerMethodField()

    class Meta:
        model = Vessel
        lookup_field = 'vessel_id'
        fields = ('vessel_id', 'locations',)
    
    def get_locations(self, obj):
        page_size = ResultPagination.page_size
        paginator = Paginator(
            Location.objects.filter(vessel__vessel_id=obj.vessel_id),
            page_size
        )
        locations = paginator.page(1)
        return LocationModelSerializer(locations, many=True).data

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