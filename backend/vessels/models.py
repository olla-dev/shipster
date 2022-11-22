from functools import cached_property
from django.db import models
from django.contrib.gis.db import models as geo
from django.contrib.gis.geos import LineString

class Vessel(models.Model):
    vessel_id = models.BigIntegerField(unique=True, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['vessel_id', 'id'], name='vessel_id_idx')
        ]
        ordering = ['-vessel_id']
    
    @cached_property
    def latest_location(self):
        '''The latest vessel location'''
        return Location.objects.filter(vessel__vessel_id=self.vessel_id).latest('received_time_utc')

    @cached_property
    def journey(self):
        '''Represents the vessels journey as a LineString'''
        locations = Location.objects.filter(vessel__vessel_id=self.vessel_id).all()
        return LineString([location.point for location in locations])

    def __str__(self):
        return "%s" % (self.vessel_id)

class Location(models.Model):
    received_time_utc = models.DateTimeField(null=False, blank=False)
    point = geo.PointField(srid=4326, null=False, blank=False)
    vessel = models.ForeignKey(
        Vessel, 
        related_name="locations", 
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=['received_time_utc', 'id'], name='received_time_utc_idx')
        ]
        ordering = ['-received_time_utc']
    
    def __str__(self):
        return "Vessel %s (%s)" % (self.vessel.vessel_id, self.received_time_utc)