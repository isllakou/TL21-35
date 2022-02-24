from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.

class Operator(models.Model):
    """
    Make a abriviation and username choice list. FOr username maybe
    """

    provider_ID = models.TextField(primary_key=True, unique = True, max_length=4, default= 'null')
    tagProvider = models.TextField(max_length=30)

    def __repr__(self):
        return self.provider_ID

class Vehicle(models.Model):
    vehicleID = models.TextField(primary_key=True)
    tagID = models.TextField(max_length=9)
    tagProvider = models.ForeignKey(Operator, on_delete=CASCADE)
    providerAbbr = models.TextField(max_length=20)
    licenseYear = models.DecimalField(max_digits=4, decimal_places=0)

    def __repr__(self):
        return self.vehicleID


class Station(models.Model):
    stationID = models.CharField(primary_key=True, max_length=5)
    stationProvider = models.CharField(max_length=30)
    stationName = models.CharField(max_length=30)

    def __repr__(self):
        return self.stationID

class Passes(models.Model):
    passID = models.TextField(primary_key=True, unique = True, max_length=10)
    timestamp = models.DateTimeField(auto_now=False)
    stationRef = models.ForeignKey(Station, on_delete= CASCADE)
    vehicleRef = models.TextField(max_length=12)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    providerAbbr = models.TextField(max_length=20, null=True)

    def __repr__(self):
        return self.passID
