from .serializers import VesselSerializer
from rest_framework import viewsets
from .models import Vessel

class VesselView(viewsets.ReadOnlyModelViewSet):
    model = Vessel
    serializer_class = VesselSerializer
    queryset = Vessel.objects.all()