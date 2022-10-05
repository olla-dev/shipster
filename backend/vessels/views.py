from .pagination import ResultPagination
from rest_framework.response import Response
from .serializers import CsvModelSerializer, LocationGeoPointSerializer, VesselModelSerializer
from rest_framework import viewsets, generics, status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.cache import cache
from django.db.models import Q

from core.settings import CACHE_TTL
from .models import Location, Vessel

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VesselView(viewsets.ReadOnlyModelViewSet):
    '''This ViewSet serves all vessel info with their latest ResultPagination.page_size recent locations'''
    model = Vessel
    serializer_class = VesselModelSerializer
    lookup_field='vessel_id'
    # Optimization: 
    # I should use a cursor pagination if a vessel has a huge list of locations.
    # will try to do it, if I finish the UI :/
    queryset = Vessel.objects.prefetch_related('locations').all()

class VesselCsvView(generics.ListAPIView):
    model = Location
    serializer_class = CsvModelSerializer
    pagination_class = ResultPagination

    def get_queryset(self):
        # check for query filter
        filter = self.request.query_params.get('filter')
        if filter is not None:
            filtered_locations = Location.objects.filter(
                Q(vessel__vessel_id__icontains = filter)
            )
            cached_rows = filtered_locations
            cache.set('csv_rows', cached_rows, CACHE_TTL)
            return cached_rows
        else:
            cached_rows = cache.get('csv_rows')
            if not cached_rows:
                cached_rows = Location.objects.select_related('vessel').all()
                cache.set('csv_rows', cached_rows, CACHE_TTL)
        
        return cached_rows

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class LocationView(viewsets.ModelViewSet):
    """
    Retrieve, update or delete a location instance.
    """
    serializer_class = LocationGeoPointSerializer
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

    def destroy(self, request, *args, **kwargs):
        try:
            location_id = self.kwargs['pk']

            if Location.objects.filter(id=location_id).exists():
                instance = Location.objects.get(id=location_id)
                instance.delete()
                # update cache
                cached_rows = Location.objects.select_related('vessel').all()
                cache.set('csv_rows', cached_rows, CACHE_TTL)
            else: 
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
        

