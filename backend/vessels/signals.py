
from django.db.models.signals import post_save
from django.dispatch import receiver
from vessels.serializers import LocationGeoPointSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Location

@receiver(post_save, sender=Location, dispatch_uid="save_location")
def vessel_location_update(sender, instance, **kwargs):
    print('Vessel Location update')
    # get latest vessel location
    latest_location = Location.objects.filter(
        vessel__vessel_id=instance.vessel.vessel_id
    ).latest('received_time_utc')
    serialized_location = LocationGeoPointSerializer(latest_location, many=False).data

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('vessels', {
        'type': 'location_update',
        'data': serialized_location
    })