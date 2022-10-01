from .pagination import ResultPagination
from .serializers import CsvModelSerializer, VesselGeoSerializer, VesselModelSerializer
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from core.settings import CACHE_TTL
from .models import Location, Vessel

@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VesselView(viewsets.ReadOnlyModelViewSet):
    model = Vessel
    pagination_class = ResultPagination
    serializer_class = VesselModelSerializer
    queryset = Vessel.objects.prefetch_related('locations').all()

@method_decorator(cache_page(CACHE_TTL), name='get')
class VesselCsvView(ListAPIView):
    model = Location
    serializer_class = CsvModelSerializer
    pagination_class = ResultPagination
    # select_related is very important here to reduce 
    # the number of db queries!!!!
    queryset = Location.objects.select_related('vessel').all()

@method_decorator(cache_page(CACHE_TTL), name='get')
class VesselGeoView(ListAPIView):
    model = Vessel
    serializer_class = VesselGeoSerializer
    pagination_class = ResultPagination
    queryset = Vessel.objects.prefetch_related('locations').all()
