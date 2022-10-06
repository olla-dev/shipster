from django.urls import re_path
from .consumers import VesselConsumer

websocket_urlpatterns = [
    re_path(r'ws/vessels', VesselConsumer.as_asgi()),
]