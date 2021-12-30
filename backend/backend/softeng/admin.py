from django.contrib import admin
"""To parakatw den to peirazoyme.
Eisagei ola ta model sto arxeio admin
gia na mhn ta eisagoyme ena ena"""
from .models import *


class ChargeAdmin(admin.ModelAdmin):
    list_display = ('tagID', 'foperator', 'operatorDebited',
        'dateOfCharge', 'amount', 'vehicleID')

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('operatorID', 'username', 'password', 'status', 'abriviation')

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoiceID', 'foperator', 'amount', 'startingDate', 'column')

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicleID', 'tagID', 'tagProvider', 'licenseYear')

class StationAdmin(admin.ModelAdmin):
    list_display = ('stationID', 'stationProvider', 'stationName')

# Register your models here.

admin.site.register(Charge, ChargeAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Station, StationAdmin)
