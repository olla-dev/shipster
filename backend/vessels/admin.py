from django.contrib import admin

from vessels.models import Vessel

class VesselAdmin(admin.ModelAdmin):
    pass

admin.site.register(Vessel, VesselAdmin)