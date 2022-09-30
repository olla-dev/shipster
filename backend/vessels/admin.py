from django.contrib import admin

from vessels.models import Location, Vessel

class VesselAdmin(admin.ModelAdmin):
    pass

class LocationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Vessel, VesselAdmin)
admin.site.register(Location, LocationAdmin)