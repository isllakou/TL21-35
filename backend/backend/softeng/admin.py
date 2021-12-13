from django.contrib import admin
"""To parakatw den to peirazoyme. 
Eisagei ola ta model sto arxeio admin 
gia na mhn ta eisagoyme ena ena"""
from .models import * 

class ChargeAdmin(admin.ModelAdmin):
    list_display = ('tagID', 'operatorDebited', 
        'dateOfCharge', 'amount', 'vehicleID')

# Register your models here.

admin.site.register(Charge, ChargeAdmin)