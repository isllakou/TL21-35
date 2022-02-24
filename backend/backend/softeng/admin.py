from django.contrib import admin

from .models import *

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('provider_ID', 'tagProvider')

class PassesAdmin(admin.ModelAdmin):
    list_display = ( 'passID', 'timestamp', 'stationRef', 'vehicleRef', 'charge', 'providerAbbr')


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicleID', 'tagID', 'tagProvider', 'providerAbbr', 'licenseYear')

class StationAdmin(admin.ModelAdmin):
    list_display = ('stationID', 'stationProvider', 'stationName')

# Register your models here.

admin.site.register(Operator, OperatorAdmin)
admin.site.register(Passes, PassesAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Station, StationAdmin)
