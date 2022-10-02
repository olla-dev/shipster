from .pagination import ResultPagination
from rest_framework.response import Response
from .serializers import CsvModelSerializer, LocationModelSerializer, VesselGeoSerializer, VesselModelSerializer
from rest_framework import viewsets, generics, status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from core.settings import CACHE_TTL
from .models import Location, Vessel

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VesselView(viewsets.ReadOnlyModelViewSet):
    '''This ViewSet serves all vessel info with their latest ResultPagination.page_size recent locations'''
    model = Vessel
    pagination_class = ResultPagination
    serializer_class = VesselModelSerializer
    lookup_field='vessel_id'
    # Optimization: 
    # I should use a cursor pagination if a vessel has a huge list of locations.
    # will try to do it, if I finish the UI :/
    queryset = Vessel.objects.prefetch_related('locations').all()

@method_decorator(cache_page(CACHE_TTL), name='get')
class VesselCsvView(generics.ListAPIView):
    model = Location
    serializer_class = CsvModelSerializer
    pagination_class = ResultPagination
    # select_related is very important here to reduce 
    # the number of db queries!!!!
    queryset = Location.objects.select_related('vessel').all()

@method_decorator(cache_page(CACHE_TTL), name='get')
class VesselGeoView(generics.ListAPIView):
    model = Vessel
    serializer_class = VesselGeoSerializer
    pagination_class = ResultPagination
    # Optimization: 
    # I should use a cursor pagination if a vessel has a huge list of locations.
    # will try to do it, if I finish the UI :/
    queryset = Vessel.objects.prefetch_related('locations').all()

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class LocationView(viewsets.ModelViewSet):
    """
    Retrieve, update or delete a location instance.
    """
    serializer_class = LocationModelSerializer
    pagination_class = ResultPagination

    def get_queryset(self):
        # here drf-nested-router appends parent name to the query param, hence use vessel_vessel_id below
        vessel_id = self.kwargs['vessel_vessel_id']
        return Location.objects.select_related('vessel').filter(vessel__vessel_id=vessel_id)
    
    def create(self, request, *args, **kwargs):
        vessel_id = self.kwargs['vessel_vessel_id']
        
        # automatically assign vessel to the new location 
        vessel = Vessel.objects.get(vessel_id=vessel_id)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save(vessel=vessel)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)