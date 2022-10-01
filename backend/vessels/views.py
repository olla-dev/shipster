from .pagination import ResultPagination
from .serializers import CsvModelSerializer, VesselGeoSerializer, VesselModelSerializer
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from .models import Location, Vessel


class VesselView(viewsets.ReadOnlyModelViewSet):
    model = Vessel
    pagination_class = ResultPagination
    serializer_class = VesselModelSerializer
    queryset = Vessel.objects.all()

class VesselCsvView(ListAPIView):
    model = Location
    serializer_class = CsvModelSerializer
    pagination_class = ResultPagination
    queryset = Location.objects.all()
    

class VesselGeoView(ListAPIView):
    model = Vessel
    serializer_class = VesselGeoSerializer
    pagination_class = ResultPagination
    queryset = Vessel.objects.all()